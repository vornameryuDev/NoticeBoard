from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
import starlette
import starlette.status
from domain.user.user_router import get_current_user
from models import Answer, Question, User
from database import get_db
from domain.answer import answer_schema
from sqlalchemy.orm import Session


router = APIRouter(prefix='/api/answer')


@router.delete('/delete', status_code=starlette.status.HTTP_204_NO_CONTENT)
def answer_delete(_answer_delete:answer_schema.AnswerDelete,
                  current_user:User=Depends(get_current_user),
                  db:Session=Depends(get_db)):
    answer = db.query(Answer).get(_answer_delete.answer_id)
    if not answer:
        raise HTTPException(
            status_code=starlette.status.HTTP_400_BAD_REQUEST,
            detail="데이터 없음"
        )
    if current_user.id != answer.user.id:
        raise HTTPException(
            status_code=starlette.status.HTTP_401_BAD_REQUEST,
            detail="권한 없음"
        )
    db.delete(answer)
    db.commit()



@router.post('/vote')
def answer_vote(_answer_vote:answer_schema.AnswerVote,
                current_user:User=Depends(get_current_user),
                db:Session=Depends(get_db)):
    answer = db.query(Answer).get(_answer_vote.answer_id)
    if not answer:
        raise HTTPException(
            status_code=starlette.status.HTTP_400_BAD_REQUEST,
            detail='없는 데이터'
        )
    answer.voter.append(current_user)
    db.add(answer)
    db.commit()
    



@router.put('/update', status_code=starlette.status.HTTP_204_NO_CONTENT)
def answer_update(_answer_update:answer_schema.AnswerModify,
                  current_user:User=Depends(get_current_user),
                  db:Session=Depends(get_db)):
    answer_id=_answer_update.answer_id
    content = _answer_update.content
    answer = db.query(Answer).filter(Answer.id==answer_id).first()
    if not answer:
        raise HTTPException(
            status_code=starlette.status.HTTP_400_BAD_REQUEST,
            detail="데이터 없음"
        )
    if current_user.id != answer.user_id:
        raise HTTPException(
            status_code=starlette.status.HTTP_401_UNAUTHORIZED,
            detail="권한없음"
        )
    answer.content = content
    answer.modify_date = datetime.now()
    db.add(answer)
    db.commit()

@router.get('/detail/{answer_id}', response_model=answer_schema.Answers)
def answer_detail(answer_id:int,
                  db:Session=Depends(get_db)):
    answer = db.query(Answer).get(answer_id)
    return answer


@router.post('/create/{question_id}', status_code=starlette.status.HTTP_204_NO_CONTENT)
def answer_create(question_id:int,
                  _answer_schema:answer_schema.AnswerCreate,
                  current_user:User=Depends(get_current_user),
                  db:Session=Depends(get_db)):
    question = db.query(Question).get(question_id)
    if not question:
        raise HTTPException(
            status_code=starlette.status.HTTP_400_BAD_REQUEST,
            detail='정보없음'
        )
    content = _answer_schema.content
    answer = Answer(
        content=content,
        create_date=datetime.now(),
        user=current_user,
        question=question
    )
    db.add(answer)
    db.commit()
    