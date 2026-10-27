from sqlmodel import Field, SQLModel


class Apartment(SQLModel, table=True):
    __tablename__ = "apartments"
    id: int | None = Field(default=None, primary_key=True)
    number: int
    floor: int