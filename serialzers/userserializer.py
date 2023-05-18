from pydantic import BaseModel, Field
from typing import Optional



class UserModelSerializer(BaseModel):
    id: Optional[str]
    username: str
    name: str
    lastname: str
    age: Optional[int]
    disable: Optional[bool]
    password: str


    class Config:
        fields = {
            'id': Field(..., alias='_id'),
            'disable': Field(default=False, alias='is_disabled')
        }
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "pedro",
                "name": "Pedro",
                "lastname": "Perez",
                "age": 15,
                "disable": False
            }
        }

class PasswordModelSerializer(BaseModel):
    id: int
    password: str

    class Config:
        orm_mode = True

    