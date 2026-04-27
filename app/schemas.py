from pydantic import BaseModel
from datetime import datetime


# схема для отдачи вакансии в апи
class VacancyOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    salary: int | None = None
    is_active: bool
    employer_name: str | None = None  # имя работодателя для карточки на фронте

    # говорим pydantic читать данные из атрибутов sqlalchemy объекта
    model_config = {"from_attributes": True}

# схемы для подачи и просмотра заявки
class ApplicationCreate(BaseModel):
    vacancy_id: int
    cover_letter: str | None = None


class ApplicationOut(BaseModel):
    id: int
    vacancy_id: int
    user_id: int
    cover_letter: str | None = None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}