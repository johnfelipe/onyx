from typing import Any

from danswer.configs.app_configs import DISABLE_GENERATIVE_AI
from danswer.configs.chat_configs import QA_TIMEOUT
from danswer.configs.model_configs import GEN_AI_MODEL_FALLBACK_MAX_TOKENS
from danswer.configs.model_configs import GEN_AI_TEMPERATURE
from danswer.db.engine import get_session_context_manager
from danswer.db.llm import fetch_default_provider
from danswer.db.llm import fetch_provider
from danswer.db.models import Persona
from danswer.llm.chat_llm import DefaultMultiLLM
from danswer.llm.exceptions import GenAIDisabledException
from danswer.llm.interfaces import LLM
from danswer.llm.override_models import LLMOverride
from danswer.utils.headers import build_llm_extra_headers
from danswer.utils.long_term_log import LongTermLogger


def _build_extra_model_kwargs(provider: str) -> dict[str, Any]:
    """Ollama requires us to specify the max context window.

    For now, just using the GEN_AI_MODEL_FALLBACK_MAX_TOKENS value.
    TODO: allow model-specific values to be configured via the UI.
    """
    return {"num_ctx": GEN_AI_MODEL_FALLBACK_MAX_TOKENS} if provider == "ollama" else {}


def get_main_llm_from_tuple(
    llms: tuple[LLM, LLM],
) -> LLM:
    return llms[0]


def get_llms_for_persona(
    persona: Persona,
    llm_override: LLMOverride | None = None,
    additional_headers: dict[str, str] | None = None,
    long_term_logger: LongTermLogger | None = None,
) -> tuple[LLM, LLM]:
    model_provider_override = llm_override.model_provider if llm_override else None
    model_version_override = llm_override.model_version if llm_override else None
    temperature_override = llm_override.temperature if llm_override else None

    provider_name = model_provider_override or persona.llm_model_provider_override
    if not provider_name:
        return get_default_llms(
            temperature=temperature_override or GEN_AI_TEMPERATURE,
            additional_headers=additional_headers,
            long_term_logger=long_term_logger,
        )

    with get_session_context_manager() as db_session:
        llm_provider = fetch_provider(db_session, provider_name)

    if not llm_provider:
        raise ValueError("No LLM provider found")

    model = model_version_override or persona.llm_model_version_override
    fast_model = llm_provider.fast_default_model_name or llm_provider.default_model_name
    if not model:
        raise ValueError("No model name found")
    if not fast_model:
        raise ValueError("No fast model name found")

    def _create_llm(model: str) -> LLM:
        return get_llm(
            provider=llm_provider.provider,
            model=model,
            deployment_name=llm_provider.deployment_name,
            api_key=llm_provider.api_key,
            api_base=llm_provider.api_base,
            api_version=llm_provider.api_version,
            custom_config=llm_provider.custom_config,
            temperature=temperature_override,
            additional_headers=additional_headers,
            long_term_logger=long_term_logger,
        )

    return _create_llm(model), _create_llm(fast_model)


def get_default_llms(
    timeout: int = QA_TIMEOUT,
    temperature: float = GEN_AI_TEMPERATURE,
    additional_headers: dict[str, str] | None = None,
    long_term_logger: LongTermLogger | None = None,
) -> tuple[LLM, LLM]:
    if DISABLE_GENERATIVE_AI:
        raise GenAIDisabledException()

    with get_session_context_manager() as db_session:
        llm_provider = fetch_default_provider(db_session)

    if not llm_provider:
        raise ValueError("No default LLM provider found")

    model_name = llm_provider.default_model_name
    fast_model_name = (
        llm_provider.fast_default_model_name or llm_provider.default_model_name
    )
    if not model_name:
        raise ValueError("No default model name found")
    if not fast_model_name:
        raise ValueError("No fast default model name found")

    def _create_llm(model: str) -> LLM:
        return get_llm(
            provider=llm_provider.provider,
            model=model,
            deployment_name=llm_provider.deployment_name,
            api_key=llm_provider.api_key,
            api_base=llm_provider.api_base,
            api_version=llm_provider.api_version,
            custom_config=llm_provider.custom_config,
            timeout=timeout,
            temperature=temperature,
            additional_headers=additional_headers,
            long_term_logger=long_term_logger,
        )

    return _create_llm(model_name), _create_llm(fast_model_name)


def get_llm(
    provider: str,
    model: str,
    deployment_name: str | None,
    api_key: str | None = None,
    api_base: str | None = None,
    api_version: str | None = None,
    custom_config: dict[str, str] | None = None,
    temperature: float | None = None,
    timeout: int = QA_TIMEOUT,
    additional_headers: dict[str, str] | None = None,
    long_term_logger: LongTermLogger | None = None,
) -> LLM:
    if temperature is None:
        temperature = GEN_AI_TEMPERATURE
    return DefaultMultiLLM(
        model_provider=provider,
        model_name=model,
        deployment_name=deployment_name,
        api_key=api_key,
        api_base=api_base,
        api_version=api_version,
        timeout=timeout,
        temperature=temperature,
        custom_config=custom_config,
        extra_headers=build_llm_extra_headers(additional_headers),
        model_kwargs=_build_extra_model_kwargs(provider),
        long_term_logger=long_term_logger,
    )
