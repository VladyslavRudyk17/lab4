from sqlmodel import Field, SQLModel


class Resident(SQLModel, table=True):
    __tablename__ = "residents"
    id: int | None = Field(default=None, primary_key=True)
    full_name: str
    phone: str = Field(regex=r"^\+380\d{9}$") # Тільки українські номери
    email: str = Field(regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    apartment_id: int | None = Field(default=None, foreign_key="apartments.id")
