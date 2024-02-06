from pydantic import BaseModel

from src.models import Role


class TestSuperUser(BaseModel):
    email: str
    hashed_password: str
    first_name: str | None
    last_name: str | None
    role: list[Role]