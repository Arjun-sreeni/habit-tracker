"""add index for foriegn keys

Revision ID: 76cca2072cb6
Revises: 5921a5a3e025
Create Date: 2026-04-06 09:06:38.204382
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "76cca2072cb6"
down_revision: Union[str, Sequence[str], None] = "5921a5a3e025"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Index for habit_logs.habit_id
    op.create_index(
        op.f("ix_habit_logs_habit_id"), "habit_logs", ["habit_id"], unique=False
    )

    # Recreate FK with CASCADE
    op.drop_constraint("habit_logs_habit_id_fkey", "habit_logs", type_="foreignkey")
    op.create_foreign_key(
        "habit_logs_habit_id_fkey",
        "habit_logs",
        "habits",
        ["habit_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Index for habits.user_id
    op.create_index(op.f("ix_habits_user_id"), "habits", ["user_id"], unique=False)

    # Recreate FK with CASCADE
    op.drop_constraint("habits_user_id_fkey", "habits", type_="foreignkey")
    op.create_foreign_key(
        "habits_user_id_fkey",
        "habits",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    # Remove FK (habits → users)
    op.drop_constraint("habits_user_id_fkey", "habits", type_="foreignkey")
    op.create_foreign_key("habits_user_id_fkey", "habits", "users", ["user_id"], ["id"])

    op.drop_index(op.f("ix_habits_user_id"), table_name="habits")

    # Remove FK (habit_logs → habits)
    op.drop_constraint("habit_logs_habit_id_fkey", "habit_logs", type_="foreignkey")
    op.create_foreign_key(
        "habit_logs_habit_id_fkey", "habit_logs", "habits", ["habit_id"], ["id"]
    )

    op.drop_index(op.f("ix_habit_logs_habit_id"), table_name="habit_logs")
