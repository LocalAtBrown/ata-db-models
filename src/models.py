from sqlmodel import Field, SQLModel


class Events(SQLModel, table=True):
    id: str = Field(primary_key=True)
    partner: str
    # TODO so many more columns
