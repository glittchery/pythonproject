from pydantic import BaseModel, Field, EmailStr, ConfigDict
from fastapi import FastAPI

app = FastAPI()

data = {
    "email": "abc@mail.ru",
    "bio": "mememe",
}

class UserSchema(BaseModel):
    email: EmailStr
    bio: str = Field(max_length=1000)
    model_config = ConfigDict(extra="forbid")


users = []

@app.post("/users")
def add_user(user: UserSchema):
    users.append(user)
    return {"ok": True, "message": "User добавлен"}

@app.get("/users")
def get_user() -> list[UserSchema]:
    return users



# class UserAgeSchema(UserSchema):
#     age: int = Field(ge=0, le=130)
#
#

