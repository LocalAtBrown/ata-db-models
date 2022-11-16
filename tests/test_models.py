from sqlmodel import create_engine

from src.models import SQLModel


def test_create_tables():
    # if it runs and no errors pop up, congrats, the tables were made without error
    db_engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
    SQLModel.metadata.create_all(db_engine)
