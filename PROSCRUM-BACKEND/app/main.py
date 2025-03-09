from fastapi import FastAPI, Depends, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware

import time

from sqlalchemy.orm import Session

import psycopg2
from psycopg2.extras import RealDictCursor

from .routers import round, course
from . import schemas, models
from .database import engine, get_db

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
        time.sleep(2)

@app.get("/")
def home():
    return {"message": "Hello Golf!"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    users = db.query(schemas.User).all()
    print(users)
    return{"result": users}

@app.post("/sqlalchemy", status_code=status.HTTP_201_CREATED)
def create_user(user: models.UserCreate, db: Session = Depends(get_db)):
    new_user = schemas.User(**user.model_dump())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"result": new_user}

@app.get("/sqlalchemy/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(schemas.User).filter(schemas.User.user_id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")

    return {"result": user}

@app.delete("/sqlalchemy/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    delete_query = db.query(schemas.User).filter(schemas.User.user_id == id)

    if delete_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    
    delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/sqlalchemy/{id}")
def update_user(id: int, user: models.UserUpdate, db: Session = Depends(get_db)):
    user_query = db.query(schemas.User).filter(schemas.User.user_id == id)

    updated_user = user_query.first()

    if updated_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    
    user_query.update(user.model_dump(), synchronize_session=False)

    db.commit()

    return {"result": user_query.first()}


app.include_router(course.router)
app.include_router(round.router)