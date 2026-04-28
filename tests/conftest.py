import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app import models


# отдельная тестовая бд
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def db_session():
    # StaticPool, чтобы все запросы шли через одно соединение
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    Base.metadata.create_all(bind=engine)

    session = TestSession()

    # засеваем минимальные данные - юзер и вакансия с работодателем
    user = models.User(id=1, full_name="Тест Тестов", email="test@test.ru", role="student")
    employer = models.Employer(id=1, name="Тестовый работодатель", type="department")
    category = models.Category(id=1, name="тест-категория")
    session.add_all([user, employer, category])
    session.commit()

    vacancy = models.Vacancy(id=1, title="Тест-вакансия", description="описание",
                              employer_id=1, category_id=1, salary=10000, is_active=True)
    session.add(vacancy)
    session.commit()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()