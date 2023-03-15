from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    language_id = Column(Integer, ForeignKey("language.id"))

    language = relationship("Language", back_populates="courses")


class Language(Base):
    __tablename__ = "language"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    courses = relationship("Course", back_populates="language")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    activated = Column(Boolean, default=False)


class UserPasswordReminder(Base):
    __tablename__ = "userpasswordreminder"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    code = Column(String)
