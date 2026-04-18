def test_get_questions_returns_questions(client, seed_data):
    response = client.get("/questions")

    assert response.status_code == 200

    data = response.json()
    assert "questions" in data
    assert len(data["questions"]) > 0

    first_question = data["questions"][0]
    assert "id" in first_question
    assert "code" in first_question
    assert "title" in first_question
    assert "options" in first_question
    assert len(first_question["options"]) > 0