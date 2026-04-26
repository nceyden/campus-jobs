from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)  # студент или админ
    created_at = Column(DateTime, default=datetime.utcnow)

    applications = relationship("Application", back_populates="user")
    resume = relationship("Resume", back_populates="user", uselist=False)
    notifications = relationship("Notification", back_populates="user")


class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String)  # department, lab, partner
    contact = Column(String)

    vacancies = relationship("Vacancy", back_populates="employer")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    vacancies = relationship("Vacancy", back_populates="category")


class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    salary = Column(Integer)  # может быть null если без оплаты
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    employer = relationship("Employer", back_populates="vacancies")
    category = relationship("Category", back_populates="vacancies")
    applications = relationship("Application", back_populates="vacancy")
    skills = relationship("VacancySkill", back_populates="vacancy")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    vacancies = relationship("VacancySkill", back_populates="skill")


class VacancySkill(Base):
    __tablename__ = "vacancy_skills"

    # составной ключ из двух FK
    vacancy_id = Column(Integer, ForeignKey("vacancies.id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), primary_key=True)

    vacancy = relationship("Vacancy", back_populates="skills")
    skill = relationship("Skill", back_populates="vacancies")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)  # один к одному
    content = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resume")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    vacancy_id = Column(Integer, ForeignKey("vacancies.id"))
    cover_letter = Column(Text)
    status = Column(String, nullable=False, default="new")  # new, reviewing, accepted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="applications")
    vacancy = relationship("Vacancy", back_populates="applications")
    interviews = relationship("Interview", back_populates="application")


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    scheduled_at = Column(DateTime, nullable=False)
    location = Column(String)
    status = Column(String, default="planned")  # planned, done, cancelled

    application = relationship("Application", back_populates="interviews")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    target_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # отзыв на студента
    employer_id = Column(Integer, ForeignKey("employers.id"), nullable=True)  # отзыв на работодателя
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")