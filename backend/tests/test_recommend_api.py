def test_post_recommend_returns_recommendations(client, seed_data):
    payload = {
        "answers": [
            {
                "questionId": seed_data["question_id"],
                "optionId": seed_data["option_story_id"],
            }
        ]
    }

    response = client.post("/recommend", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) > 0

    first_item = data["recommendations"][0]
    assert "gameId" in first_item
    assert "name" in first_item
    assert "reason" in first_item


def test_post_recommend_rejects_invalid_answer(client, seed_data):
    payload = {
        "answers": [
            {
                "questionId": 999999,
                "optionId": 999999,
            }
        ]
    }

    response = client.post("/recommend", json=payload)

    assert response.status_code == 400