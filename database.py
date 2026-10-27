from fastapi import FastAPI
from sqlmodel import Session, create_engine

# Підключення до локальної БД
engine = create_engine("postgresql+psycopg://postgres:postgress@localhost:5432/postgres")
app = FastAPI(title="ОСББ API")
def get_session():
    with Session(engine) as session:
        yield session