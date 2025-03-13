from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import psycopg2
from psycopg2.extras import RealDictCursor

from .routers import round, course, user, auth, scorecard
from . import schemas
from .database import engine

schemas.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Connection to database

while True:
    try:
        connection = psycopg2.connect(host='localhost', database='proscrum-golf', user='postgres', password='1234', cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connecting to database failed.")
        print("Error: ", error)
        break

@app.get("/")
def home():
    return {"message": "Hello Golf!"}

app.include_router(user.router)
app.include_router(course.router)
app.include_router(round.router)
app.include_router(auth.router)
app.include_router(scorecard.router)
