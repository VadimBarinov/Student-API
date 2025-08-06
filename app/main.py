from fastapi import FastAPI
from app.students.router import router as router_students
from app.majors.router import router as router_majors
from app.study_groups.router import router as router_study_groups
from app.weekdays.router import router as router_weekdays
from app.subjects.router import router as router_subjects
from app.teachers.router import router as router_teachers
from app.lessons.router import router as router_lessons


app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Привет, Друг!"}


# Подключение роутеров
app.include_router(router_students)
app.include_router(router_majors)
app.include_router(router_study_groups)
app.include_router(router_weekdays)
app.include_router(router_subjects)
app.include_router(router_teachers)
app.include_router(router_lessons)