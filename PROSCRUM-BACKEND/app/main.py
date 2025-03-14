from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def home():
    return {"message": "Hello Golf!"}

app.include_router(user.router)
app.include_router(course.router)
app.include_router(round.router)
app.include_router(auth.router)
app.include_router(scorecard.router)
