from collections.abc import Mapping
from typing import Any
from typing import cast

from onyx.auth.schemas import UserRole
from onyx.configs.constants import KV_NO_AUTH_USER_PREFERENCES_KEY
from onyx.key_value_store.store import KeyValueStore
from onyx.key_value_store.store import KvKeyNotFoundError
from onyx.server.manage.models import UserInfo
from onyx.server.manage.models import UserPreferences


def set_no_auth_user_preferences(
    store: KeyValueStore, preferences: UserPreferences
) -> None:
    store.store(KV_NO_AUTH_USER_PREFERENCES_KEY, preferences.model_dump())


def load_no_auth_user_preferences(store: KeyValueStore) -> UserPreferences:
    try:
        preferences_data = cast(
            Mapping[str, Any], store.load(KV_NO_AUTH_USER_PREFERENCES_KEY)
        )
        return UserPreferences(**preferences_data)
    except KvKeyNotFoundError:
        return UserPreferences(
            chosen_assistants=None, default_model=None, auto_scroll=True
        )


def fetch_no_auth_user(store: KeyValueStore) -> UserInfo:
    return UserInfo(
        id="__no_auth_user__",
        email="anonymous@onyx.app",
        is_active=True,
        is_superuser=False,
        is_verified=True,
        role=UserRole.ADMIN,
        preferences=load_no_auth_user_preferences(store),
    )
