from sqlmodel import Session, delete

from app.db.engine import engine
from app.db.models import OptionTagWeight, QuestionOption, Question


def reset_questionnaire_seed_data() -> None:
    with Session(engine) as session:
        session.exec(delete(OptionTagWeight))
        session.exec(delete(QuestionOption))
        session.exec(delete(Question))
        session.commit()

    print("Questionnaire seed data reset completed.")


if __name__ == "__main__":
    reset_questionnaire_seed_data()