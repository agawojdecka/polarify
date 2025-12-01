from pydantic import BaseModel


# Common user model
class User(BaseModel):
    username: str
    email: str
