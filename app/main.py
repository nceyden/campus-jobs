from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, SessionLocal
from app import models, schemas

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


@app.get("/vacancies", response_model=list[schemas.VacancyOut])
def get_vacancies(db: Session = Depends(get_db)):
    return db.query(models.Vacancy).all()


CURRENT_USER_ID = 1 # хардкодим текущего юзера, без авторизации


@app.post("/applications", response_model=schemas.ApplicationOut, status_code=201)
def create_application(data: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    vacancy = db.query(models.Vacancy).filter(models.Vacancy.id == data.vacancy_id).first()  # проверяем что вакансия существует
    if not vacancy:
        raise HTTPException(status_code=404, detail="вакансия не найдена")

    existing = db.query(models.Application).filter(     # один юзер - одна заявка на вакансию
        models.Application.user_id == CURRENT_USER_ID,
        models.Application.vacancy_id == data.vacancy_id,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="заявка уже подана")

    application = models.Application(
        user_id=CURRENT_USER_ID,
        vacancy_id=data.vacancy_id,
        cover_letter=data.cover_letter,
        status="new",
    )
    db.add(application)
    db.commit()
    db.refresh(application)  # подтянем сгенерированный id и created_at
    return application


@app.get("/me/applications", response_model=list[schemas.ApplicationOut])
def get_my_applications(db: Session = Depends(get_db)):
    return db.query(models.Application).filter(
        models.Application.user_id == CURRENT_USER_ID
    ).all()