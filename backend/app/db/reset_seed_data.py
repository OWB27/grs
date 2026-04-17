from sqlmodel import Session
from sqlalchemy import text

from app.db.engine import engine


RESET_SQL = """
TRUNCATE TABLE
  game_tags,
  option_tag_weights,
  question_options,
  games,
  tags,
  questions
RESTART IDENTITY CASCADE;
"""


def reset_seed_data() -> None:
    with Session(engine) as session:
        session.execute(text(RESET_SQL))
        session.commit()

    print("Seed data reset completed.")


if __name__ == "__main__":
    reset_seed_data()