"""testing

Revision ID: 5be3aa848ce8
Revises: bceb1e139447
Create Date: 2024-08-28 17:15:06.247199

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5be3aa848ce8"
down_revision = "bceb1e139447"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "chat_message__standard_answer",
        sa.Column("chat_message_id", sa.Integer(), nullable=False),
        sa.Column("standard_answer_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["chat_message_id"],
            ["chat_message.id"],
        ),
        sa.ForeignKeyConstraint(
            ["standard_answer_id"],
            ["standard_answer.id"],
        ),
        sa.PrimaryKeyConstraint("chat_message_id", "standard_answer_id"),
    )
    op.drop_table("kombu_queue")
    op.drop_index("ix_kombu_message_timestamp", table_name="kombu_message")
    op.drop_index("ix_kombu_message_timestamp_id", table_name="kombu_message")
    op.drop_index("ix_kombu_message_visible", table_name="kombu_message")
    op.drop_table("kombu_message")
    op.create_foreign_key(None, "api_key", "user", ["user_id"], ["id"])
    op.create_foreign_key(None, "api_key", "user", ["owner_id"], ["id"])
    op.alter_column(
        "chat_folder",
        "display_priority",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.drop_constraint("chat_message_id_key", "chat_message", type_="unique")
    op.alter_column(
        "credential",
        "source",
        existing_type=sa.VARCHAR(length=100),
        nullable=False,
    )
    op.alter_column(
        "credential",
        "credential_json",
        existing_type=postgresql.BYTEA(),
        nullable=False,
    )
    op.drop_index(
        "ix_document_by_connector_credential_pair_pkey__connecto_27dc",
        table_name="document_by_connector_credential_pair",
    )
    op.alter_column(
        "document_set__user", "user_id", existing_type=sa.UUID(), nullable=True
    )
    op.add_column(
        "email_to_external_user_cache",
        sa.Column(
            "source_type",
            sa.Enum(
                "INGESTION_API",
                "SLACK",
                "WEB",
                "GOOGLE_DRIVE",
                "GMAIL",
                "REQUESTTRACKER",
                "GITHUB",
                "GITLAB",
                "GURU",
                "BOOKSTACK",
                "CONFLUENCE",
                "SLAB",
                "JIRA",
                "PRODUCTBOARD",
                "FILE",
                "NOTION",
                "ZULIP",
                "LINEAR",
                "HUBSPOT",
                "DOCUMENT360",
                "GONG",
                "GOOGLE_SITES",
                "ZENDESK",
                "LOOPIO",
                "DROPBOX",
                "SHAREPOINT",
                "TEAMS",
                "SALESFORCE",
                "DISCOURSE",
                "AXERO",
                "CLICKUP",
                "MEDIAWIKI",
                "WIKIPEDIA",
                "S3",
                "R2",
                "GOOGLE_CLOUD_STORAGE",
                "OCI_STORAGE",
                "NOT_APPLICABLE",
                name="documentsource",
                native_enum=False,
            ),
            nullable=False,
        ),
    )
    op.alter_column(
        "inputprompt__user",
        "user_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.alter_column(
        "llm_provider", "provider", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column("persona__user", "user_id", existing_type=sa.UUID(), nullable=True)
    op.alter_column(
        "saml",
        "expires_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
    )
    op.alter_column(
        "search_settings",
        "query_prefix",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "search_settings",
        "passage_prefix",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "search_settings", "status", existing_type=sa.VARCHAR(), nullable=False
    )
    op.create_index(
        "ix_embedding_model_future_unique",
        "search_settings",
        ["status"],
        unique=True,
        postgresql_where=sa.text("status = 'FUTURE'"),
    )
    op.create_index(
        "ix_embedding_model_present_unique",
        "search_settings",
        ["status"],
        unique=True,
        postgresql_where=sa.text("status = 'PRESENT'"),
    )
    op.drop_constraint("standard_answer_keyword_key", "standard_answer", type_="unique")
    op.create_index(
        "unique_keyword_active",
        "standard_answer",
        ["keyword", "active"],
        unique=True,
        postgresql_where=sa.text("active = true"),
    )
    op.alter_column(
        "tool_call",
        "tool_result",
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        nullable=True,
    )
    op.alter_column(
        "user__user_group", "user_id", existing_type=sa.UUID(), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user__user_group", "user_id", existing_type=sa.UUID(), nullable=False
    )
    op.alter_column(
        "tool_call",
        "tool_result",
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        nullable=False,
    )
    op.drop_index(
        "unique_keyword_active",
        table_name="standard_answer",
        postgresql_where=sa.text("active = true"),
    )
    op.create_unique_constraint(
        "standard_answer_keyword_key", "standard_answer", ["keyword"]
    )
    op.drop_index(
        "ix_embedding_model_present_unique",
        table_name="search_settings",
        postgresql_where=sa.text("status = 'PRESENT'"),
    )
    op.drop_index(
        "ix_embedding_model_future_unique",
        table_name="search_settings",
        postgresql_where=sa.text("status = 'FUTURE'"),
    )
    op.alter_column(
        "search_settings", "status", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "search_settings",
        "passage_prefix",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )
    op.alter_column(
        "search_settings",
        "query_prefix",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )
    op.alter_column(
        "saml",
        "expires_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
    )
    op.alter_column("persona__user", "user_id", existing_type=sa.UUID(), nullable=False)
    op.alter_column(
        "llm_provider", "provider", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "inputprompt__user",
        "user_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.drop_column("email_to_external_user_cache", "source_type")
    op.alter_column(
        "document_set__user",
        "user_id",
        existing_type=sa.UUID(),
        nullable=False,
    )
    op.create_index(
        "ix_document_by_connector_credential_pair_pkey__connecto_27dc",
        "document_by_connector_credential_pair",
        ["connector_id", "credential_id"],
        unique=False,
    )
    op.alter_column(
        "credential",
        "credential_json",
        existing_type=postgresql.BYTEA(),
        nullable=True,
    )
    op.alter_column(
        "credential",
        "source",
        existing_type=sa.VARCHAR(length=100),
        nullable=True,
    )
    op.create_unique_constraint("chat_message_id_key", "chat_message", ["id"])
    op.alter_column(
        "chat_folder",
        "display_priority",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.drop_constraint(None, "api_key", type_="foreignkey")
    op.drop_constraint(None, "api_key", type_="foreignkey")
    op.create_table(
        "kombu_message",
        sa.Column("id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("visible", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column(
            "timestamp",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("payload", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column("version", sa.SMALLINT(), autoincrement=False, nullable=False),
        sa.Column("queue_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["queue_id"], ["kombu_queue.id"], name="FK_kombu_message_queue"
        ),
        sa.PrimaryKeyConstraint("id", name="kombu_message_pkey"),
    )
    op.create_index(
        "ix_kombu_message_visible", "kombu_message", ["visible"], unique=False
    )
    op.create_index(
        "ix_kombu_message_timestamp_id",
        "kombu_message",
        ["timestamp", "id"],
        unique=False,
    )
    op.create_index(
        "ix_kombu_message_timestamp",
        "kombu_message",
        ["timestamp"],
        unique=False,
    )
    op.create_table(
        "kombu_queue",
        sa.Column("id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("name", sa.VARCHAR(length=200), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="kombu_queue_pkey"),
        sa.UniqueConstraint("name", name="kombu_queue_name_key"),
    )
    op.drop_table("chat_message__standard_answer")
    # ### end Alembic commands ###