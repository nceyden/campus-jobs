from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./campus_jobs.db"

# check_same_thread - для sqlite, чтобы фастапи мог в нее ходить из разных потоков
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# фабрика сессий, через них работаем с бд
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# базовый класс для всех моделей
Base = declarative_base()

# зависимость для эндпоинтов: дать сессию бд и закрыть после
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()