from sqlmodel import Field, SQLModel


class Customer(SQLModel, table=True):  # type: ignore
    """The customer model."""

    id: int | None = Field(default=None, primary_key=True)
    customer_name: str
    email: str
    age: int
    gender: str
    location: str
    job: str
    salary: int
