def test_get_vacancies_returns_list(client):
    response = client.get("/vacancies")    # проверяем что GET /vacancies возвращает список вакансий

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1  # в фикстуре насеяли одну вакансию
    assert data[0]["title"] == "Тест-вакансия"
    assert data[0]["salary"] == 10000