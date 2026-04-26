from app.database import SessionLocal
from app.models import User, Employer, Category, Vacancy


def seed():
    db = SessionLocal()

    # не дублируем данные
    if db.query(Vacancy).count() > 0:
        print("данные уже есть")
        db.close()
        return

    # юзер
    student = User(full_name="Денис Голиков", email="denis@example.com", role="student")
    db.add(student)

    # работодатели
    emp1 = Employer(name="Кафедра прикладной математики", type="department", contact="math@univ.ru")
    emp2 = Employer(name="Лаборатория ИИ", type="lab", contact="ai-lab@univ.ru")
    db.add_all([emp1, emp2])

    # категории
    cat1 = Category(name="ассистент")
    cat2 = Category(name="стажировка")
    cat3 = Category(name="админ-помощь")
    db.add_all([cat1, cat2, cat3])

    db.commit()  # коммитим чтобы у emp и cat появились id

    # вакансии
    vacancies = [
        Vacancy(title="Ассистент кафедры", description="помощь с проверкой работ",
                employer_id=emp1.id, category_id=cat1.id, salary=15000),
        Vacancy(title="Стажер в лабораторию ИИ", description="разметка датасетов, работа с python",
                employer_id=emp2.id, category_id=cat2.id, salary=25000),
        Vacancy(title="Помощник на конференции", description="регистрация участников, орг вопросы",
                employer_id=emp1.id, category_id=cat3.id, salary=None),
    ]
    db.add_all(vacancies)
    db.commit()

    print(f"добавлено: {len(vacancies)} вакансии, 2 работодателя, 3 категории, 1 юзер")
    db.close()


if __name__ == "__main__":
    seed()