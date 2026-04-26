from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import Base, engine, SessionLocal
from app import models

# создаем таблицы при старте если их еще нет
Base.metadata.create_all(bind=engine)

app = FastAPI(title="campus-jobs")


# зависимость для эндпоинтов, дать сессию бд и закрыть после
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/vacancies")
def get_vacancies(db: Session = Depends(get_db)):
    vacancies = db.query(models.Vacancy).all()
    return [
        {
            "id": v.id,
            "title": v.title,
            "description": v.description,
            "salary": v.salary,
            "is_active": v.is_active,
        }
        for v in vacancies
    ]