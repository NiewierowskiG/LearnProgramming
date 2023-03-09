from fastapi import Depends, FastAPI, HTTPException
from sql_app import crud, models, schemas
from sqlalchemy.orm import Session
from sql_app.database import SessionLocal, engine
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]

models.Base.metadata.create_all(bind=engine)
SECRET = "b5e264739b0beac6f88cefe4f27a62d502cdf3a0a7c6e738"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = LoginManager(SECRET, '/login')

# TODO set it as a env variable


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)


# login


@app.post('/login')
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username = data.username
    password = data.password

    db_user = crud.get_user(db, username=username)
    if not db_user:
        raise InvalidCredentialsException
    elif password != db_user.password:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data={'sub': username}
    )
    return {'access_token': access_token}


@app.post('/register', response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Language with that name exists")
    return crud.create_user(db, user=user)


# Languages


@app.post('/language/', response_model=schemas.Language)
def create_language(language: schemas.LanguageCreate, db: Session = Depends(get_db)):
    db_language = crud.get_language_by_name(db, name=language.name)
    if db_language:
        raise HTTPException(status_code=400, detail="Language with that name exists")
    return crud.create_language(db, language=language)


@app.get('/languages/', response_model=list[schemas.Language])
def get_languages(db: Session = Depends(get_db)):
    languages = crud.get_languages(db, skip=0, limit=100)
    return languages


@app.get('/language/{language_id}', response_model=schemas.Language)
def get_language(language_id: int, db: Session = Depends(get_db)):
    language = crud.get_language(db, language_id=language_id)
    if not language:
        raise HTTPException(status_code=400, detail="Language does not exist")
    return language


@app.get('/language_name/{name}', response_model=schemas.Language)
def get_language_name(name: str, db: Session = Depends(get_db)):
    language = crud.get_language_by_name(db=db, name=name)
    if not language:
        raise HTTPException(status_code=400, detail="Language does not exist")
    return language


#Courses


@app.post('/course/{language_id}', response_model=schemas.Course)
def create_course(language_id: int, course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_language = crud.get_course_by_name(db, name=course.name)
    if db_language:
        raise HTTPException(status_code=400, detail="Course with that name exists")
    return crud.create_course(db, course=course, language_id=language_id)


@app.get('/courses/', response_model=list[schemas.Course])
def get_courses(db: Session = Depends(get_db)):
    courses = crud.get_courses(db, skip=0, limit=100)
    return courses


@app.get('/course/{course_id}', response_model=schemas.Course)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course(db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=400, detail="Course does not exist")
    return course


@app.get('/course_name/{name}', response_model=schemas.Course)
def get_course_name(name: str, db: Session = Depends(get_db)):
    course = crud.get_course_by_name(db=db, name=name)
    if not course:
        raise HTTPException(status_code=400, detail="Course does not exist")
    return course
