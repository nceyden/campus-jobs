def test_get_vacancies_returns_list(client):
    response = client.get("/vacancies")    # проверяем что GET /vacancies возвращает список вакансий

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1  # в фикстуре насеяли одну вакансию
    assert data[0]["title"] == "Тест-вакансия"
    assert data[0]["salary"] == 10000


def test_get_vacancy_by_id_returns_one(client): # проверяем что GET /vacancies/{id} возвращает одну вакансию
    response = client.get("/vacancies/1")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Тест-вакансия"
    assert data["employer_name"] == "Тестовый работодатель"


def test_get_vacancy_not_found_returns_404(client): # проверяем что для несуществующей вакансии возвращается 404
    response = client.get("/vacancies/999")

    assert response.status_code == 404
    assert "не найдена" in response.json()["detail"]


def test_create_application_success(client): # проверяем что POST /applications создает заявку
    payload = {
        "vacancy_id": 1,
        "cover_letter": "хочу работать"
    }
    response = client.post("/applications", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert data["vacancy_id"] == 1
    assert data["user_id"] == 1
    assert data["status"] == "new"
    assert data["cover_letter"] == "хочу работать"
    assert "id" in data
    assert "created_at" in data


def test_create_application_validation_error(client): # проверяем что pydantic валидация ловит невалидные данные
    # vacancy_id отсутствует - обязательное поле
    payload = {"cover_letter": "текст"}
    response = client.post("/applications", json=payload)

    assert response.status_code == 422


def test_create_application_vacancy_not_found(client): # проверяем 404 при создании заявки на несуществующую вакансию
    payload = {"vacancy_id": 999, "cover_letter": "текст"}
    response = client.post("/applications", json=payload)

    assert response.status_code == 404


def test_create_application_duplicate_returns_400(client): # проверяем что нельзя подать заявку дважды на одну вакансию
    payload = {"vacancy_id": 1, "cover_letter": "первая"}

    # первая подача - ок
    first = client.post("/applications", json=payload)
    assert first.status_code == 201

    # вторая - должна упасть
    second = client.post("/applications", json=payload)
    assert second.status_code == 400
    assert "уже подана" in second.json()["detail"]


def test_get_my_applications_returns_user_applications(client): # проверяем что GET /me/applications возвращает заявки текущего юзера
    # сначала создаем заявку
    client.post("/applications", json={"vacancy_id": 1, "cover_letter": "тест"})

    # теперь проверяем что она в кабинете
    response = client.get("/me/applications")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["user_id"] == 1
    assert data[0]["vacancy_id"] == 1
    assert data[0]["vacancy_title"] == "Тест-вакансия"