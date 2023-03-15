from sqlalchemy.orm import Session

from . import models, schemas


# Language

def get_language(db: Session, language_id: int):
    return db.query(models.Language).filter(models.Language.id == language_id).first()


def get_languages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Language).offset(skip).limit(limit).all()


def get_language_by_name(db: Session, name: str):
    return db.query(models.Language).filter(models.Language.name == name).first()


def create_language(db: Session, language: schemas.LanguageCreate):
    db_language = models.Language(name=language.name)
    db.add(db_language)
    db.commit()
    db.refresh(db_language)
    return db_language


# Courses


def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()


def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()


def get_course_by_name(db: Session, name: str):
    return db.query(models.Course).filter(models.Course.name == name).first()


def create_course(db: Session, course: schemas.CourseCreate, language_id: int):
    db_course = models.Course(**course.dict(), language_id=language_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def password_reminder_get(db: Session, code: str):
    return db.query(models.UserPasswordReminder).filter(models.UserPasswordReminder.code == code).first()


def create_user_password_code(db: Session, password_reminder: schemas.UserPasswordReminderCreate):
    code_duplicate = password_reminder_get(db, password_reminder.email)
    if code_duplicate:
        code_duplicate.remove()
    db_password_user = models.UserPasswordReminder(**password_reminder.dict())
    db.add(db_password_user)
    db.commit()
    db.refresh(db_password_user)
    return db_password_user

