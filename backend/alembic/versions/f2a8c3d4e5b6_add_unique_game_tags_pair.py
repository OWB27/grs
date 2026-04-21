"""add unique constraint to game_tags pair

Revision ID: f2a8c3d4e5b6
Revises: 9b6924210150
Create Date: 2026-04-21 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "f2a8c3d4e5b6"
down_revision: Union[str, Sequence[str], None] = "9b6924210150"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


CONSTRAINT_NAME = "uq_game_tags_game_id_tag_id"


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()

    if bind.dialect.name == "postgresql":
        op.execute(
            """
            DELETE FROM game_tags AS duplicate
            USING game_tags AS keeper
            WHERE duplicate.game_id = keeper.game_id
              AND duplicate.tag_id = keeper.tag_id
              AND duplicate.id > keeper.id
            """
        )
    else:
        op.execute(
            """
            DELETE FROM game_tags
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM game_tags
                GROUP BY game_id, tag_id
            )
            """
        )

    with op.batch_alter_table("game_tags") as batch_op:
        batch_op.create_unique_constraint(
            CONSTRAINT_NAME,
            ["game_id", "tag_id"],
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("game_tags") as batch_op:
        batch_op.drop_constraint(CONSTRAINT_NAME, type_="unique")
