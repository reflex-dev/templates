from typing import TypedDict


class Employee(TypedDict):
    employee_id: int
    first_name: str
    last_name: str
    email: str
    department: str
