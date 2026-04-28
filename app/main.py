from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="campus-jobs")

# cors - разрешаем запросы с любого origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app = FastAPI(title="campus-jobs")


@app.get("/vacancies", response_model=list[schemas.VacancyOut])
def get_vacancies(db: Session = Depends(get_db)):
    vacancies = db.query(models.Vacancy).all()
    # подкидываем имя работодателя в каждую вакансию
    for v in vacancies:
        v.employer_name = v.employer.name if v.employer else None
    return vacancies

@app.get("/vacancies/{vacancy_id}", response_model=schemas.VacancyOut)
def get_vacancy(vacancy_id: int, db: Session = Depends(get_db)):
    vacancy = db.query(models.Vacancy).filter(models.Vacancy.id == vacancy_id).first()
    if not vacancy:
        raise HTTPException(status_code=404, detail="вакансия не найдена")
    vacancy.employer_name = vacancy.employer.name if vacancy.employer else None
    return vacancy


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


# отдаем фронт, mount должен идти после всех api роутов чтобы они не перехватывались
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.get("/vacancy/{vacancy_id}")
def vacancy_page(vacancy_id: int):
    return FileResponse("static/vacancy.html")


@app.get("/apply/{vacancy_id}")
def apply_page(vacancy_id: int):
    return FileResponse("static/apply.html")


@app.get("/cabinet")
def cabinet_page():
    return FileResponse("static/cabinet.html")