# campus-jobs

Сервис поиска временной работы и стажировок в кампусе.

## Стек

- backend: Python 3.11+, FastAPI, SQLAlchemy, SQLite
- frontend: HTML, Bootstrap 5, ванильный JS
- тесты: pytest

## Запуск

создаем виртуальное окружение и ставим зависимости:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

наполняем бд тестовыми данными (один раз):

```powershell
python seed.py
```

запускаем сервер:

```powershell
uvicorn app.main:app --reload
```

открываем в браузере: http://127.0.0.1:8000/

документация api: http://127.0.0.1:8000/docs

## Тесты

```powershell
pytest -v
```

## Схема БД

![схема бд](docs/db_schema.png)
