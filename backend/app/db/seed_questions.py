from sqlmodel import Session, select

from app.db.engine import engine
from app.db.models import Question, QuestionOption


def seed_questions():
    with Session(engine) as session:
        existing = session.exec(select(Question)).first()
        if existing:
            print("Questions already seeded.")
            return

        q1 = Question(
            code="preferred_experience",
            sort_order=1,
            title_zh="你更喜欢哪种游戏体验？",
            title_en="What kind of game experience do you prefer?",
        )
        q2 = Question(
            code="game_pace",
            sort_order=2,
            title_zh="你更喜欢什么节奏？",
            title_en="What pace do you prefer?",
        )

        session.add(q1)
        session.add(q2)
        session.commit()
        session.refresh(q1)
        session.refresh(q2)

        options = [
            QuestionOption(
                question_id=q1.id,
                code="story_immersion",
                sort_order=1,
                text_zh="沉浸剧情",
                text_en="Immersive story",
            ),
            QuestionOption(
                question_id=q1.id,
                code="free_exploration",
                sort_order=2,
                text_zh="自由探索",
                text_en="Free exploration",
            ),
            QuestionOption(
                question_id=q1.id,
                code="competitive_challenge",
                sort_order=3,
                text_zh="挑战与对抗",
                text_en="Challenge and competition",
            ),
            QuestionOption(
                question_id=q2.id,
                code="slow_relaxed",
                sort_order=1,
                text_zh="慢节奏、轻松一些",
                text_en="Slow and relaxed",
            ),
            QuestionOption(
                question_id=q2.id,
                code="balanced_pace",
                sort_order=2,
                text_zh="节奏均衡",
                text_en="Balanced pace",
            ),
            QuestionOption(
                question_id=q2.id,
                code="fast_intense",
                sort_order=3,
                text_zh="快节奏、刺激一些",
                text_en="Fast and intense",
            ),
        ]

        for option in options:
            session.add(option)

        session.commit()
        print("Questions seeded.")


if __name__ == "__main__":
    seed_questions()