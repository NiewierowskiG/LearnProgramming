from typing import Union

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


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
