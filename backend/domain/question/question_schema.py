from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator
from models import User
from domain.user import user_schema
from domain.answer import answer_schema




class QuestionDelete(BaseModel):
    question_id: int

    
class QuestionVote(BaseModel):
    question_id: int


class QuestionCreate(BaseModel):
    subject:str
    content:str

    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈값 안되요')
        return v
    
    
class QuestionModify(QuestionCreate):
    question_id:int
    

class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime
    question_answers: list[answer_schema.Answers] = []
    user: user_schema.Users
    voter: list[user_schema.Users] = []
