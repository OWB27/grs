from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, delete

from app.db.models import Game, GameTag, OptionTagWeight, Question, QuestionOption, Tag
from app.db.session import get_session
from app.main import app


@pytest.fixture(scope="session")
def engine():
    test_engine = create_engine(
        "sqlite:///./test.db",
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(test_engine)
    yield test_engine
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture
def seed_data(engine) -> dict:
    with Session(engine) as session:
        session.exec(delete(GameTag))
        session.exec(delete(OptionTagWeight))
        session.exec(delete(QuestionOption))
        session.exec(delete(Game))
        session.exec(delete(Tag))
        session.exec(delete(Question))
        session.commit()

        tag_story = Tag(
            code="story_rich",
            name_zh="剧情沉浸",
            name_en="Story Rich",
            is_active=True,
        )
        tag_explore = Tag(
            code="exploration",
            name_zh="自由探索",
            name_en="Exploration",
            is_active=True,
        )
        tag_combat = Tag(
            code="combat",
            name_zh="战斗驱动",
            name_en="Combat",
            is_active=True,
        )
        session.add(tag_story)
        session.add(tag_explore)
        session.add(tag_combat)
        session.commit()
        session.refresh(tag_story)
        session.refresh(tag_explore)
        session.refresh(tag_combat)

        question = Question(
            code="preferred_experience",
            sort_order=1,
            title_zh="你更喜欢哪种游戏体验？",
            title_en="What kind of game experience do you prefer?",
        )
        session.add(question)
        session.commit()
        session.refresh(question)

        option_story = QuestionOption(
            question_id=question.id,
            code="story_immersion",
            sort_order=1,
            text_zh="沉浸剧情",
            text_en="Immersive story",
        )
        option_action = QuestionOption(
            question_id=question.id,
            code="action_combat",
            sort_order=2,
            text_zh="战斗挑战",
            text_en="Action and combat",
        )
        session.add(option_story)
        session.add(option_action)
        session.commit()
        session.refresh(option_story)
        session.refresh(option_action)

        game_1 = Game(
            code="witcher_3",
            steam_app_id=292030,
            steam_url="https://store.steampowered.com/app/292030/",
            name_zh="巫师 3：狂猎",
            name_en="The Witcher 3: Wild Hunt",
            cover_image_url="https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/292030/header.jpg",
            is_active=True,
        )
        game_2 = Game(
            code="hades",
            steam_app_id=1145360,
            steam_url="https://store.steampowered.com/app/1145360/",
            name_zh="黑帝斯",
            name_en="Hades",
            cover_image_url="https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1145360/header.jpg",
            is_active=True,
        )
        session.add(game_1)
        session.add(game_2)
        session.commit()
        session.refresh(game_1)
        session.refresh(game_2)

        session.add(
            OptionTagWeight(
                option_id=option_story.id,
                tag_id=tag_story.id,
                weight=5,
            )
        )
        session.add(
            OptionTagWeight(
                option_id=option_story.id,
                tag_id=tag_explore.id,
                weight=3,
            )
        )
        session.add(
            OptionTagWeight(
                option_id=option_action.id,
                tag_id=tag_combat.id,
                weight=5,
            )
        )

        session.add(
            GameTag(
                game_id=game_1.id,
                tag_id=tag_story.id,
                weight=5,
            )
        )
        session.add(
            GameTag(
                game_id=game_1.id,
                tag_id=tag_explore.id,
                weight=4,
            )
        )
        session.add(
            GameTag(
                game_id=game_2.id,
                tag_id=tag_combat.id,
                weight=5,
            )
        )
        session.commit()

        return {
            "question_id": question.id,
            "option_story_id": option_story.id,
            "option_action_id": option_action.id,
        }


@pytest.fixture
def client(engine) -> Generator[TestClient, None, None]:
    def override_get_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()