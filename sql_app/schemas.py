from typing import Union, Optional

from pydantic import BaseModel


class CourseBase(BaseModel):
    name: str


class CourseCreate(CourseBase):
    pass


class Course(CourseBase):
    id: int
    language_id: int

    class Config:
        orm_mode = True


class LanguageBase(BaseModel):
    name: str


class LanguageCreate(LanguageBase):
    pass


class Language(LanguageBase):
    id: int
    courses: list[Course] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    password: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    activated: Optional[bool] = False

    class Config:
        orm_mode = True


class UserPasswordReminderBase(BaseModel):
    email: str
    code: str


class UserPasswordReminderCreate(UserPasswordReminderBase):
    pass


class UserPasswordReminder(UserPasswordReminderBase):
    id: int

    class Config:
        orm_mode = True
