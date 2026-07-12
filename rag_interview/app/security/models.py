from pydantic import BaseModel


class CurrentUser(BaseModel):
    id: str
    name: str | None = None
    email: str | None = None
    roles: list[str] = []