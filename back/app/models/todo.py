from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("유효하지 않은 ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class TodoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    text: str
    completed: bool = False

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class TodoCreateModel(BaseModel):
    text: str
    completed: bool = False

class TodoUpdateModel(BaseModel):
    text: Optional[str] = None
    completed: Optional[bool] = None 