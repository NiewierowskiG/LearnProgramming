from fastapi import Depends, FastAPI, HTTPException
from sql_app import crud, models, schemas
from sqlalchemy.orm import Session
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
models.Base.metadata.create_all(bind=engine)


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
