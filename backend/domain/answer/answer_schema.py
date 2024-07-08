from datetime import datetime
from pydantic import BaseModel, field_validator
from domain.user import user_schema



class AnswerDelete(BaseModel):
    answer_id:int

class AnswerVote(BaseModel):
    answer_id:int

class AnswerCreate(BaseModel):
    content: str

    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈값안되요~')
        return v


class AnswerModify(AnswerCreate):
    answer_id:int
    

class Answers(BaseModel):
    id: int
    content: str
    create_date: datetime
    user: user_schema.Users
    question_id: int
    voter: list[user_schema.Users] = []
