from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
import starlette.status
from domain.user.user_router import get_current_user
from domain.question import question_schema
from models import Answer, Question, User
from database import SessionLocal, get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix='/api/question')



@router.delete('/delete', status_code=starlette.status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete:question_schema.QuestionDelete,
                    current_user:User=Depends(get_current_user),
                    db:Session=Depends(get_db)):
    question = db.query(Question).get(_question_delete.question_id)
    if not question:
        raise HTTPException(
            status_code=starlette.status.HTTP_400_BAD_REQUEST,
            detail="데이터 없음"
        )
    if current_user.id != question.user.id:
        raise HTTPException(
            status_code=starlette.status.HTTP_401_UNAUTHORIZED,
            detail="권한 없음"
        )
    db.delete(question)
    db.commit()



@router.post('/vote')
def question_vote(_question_vote:question_schema.QuestionVote,
                  current_user:User=Depends(get_current_user),
                  db:Session=Depends(get_db)):
    question = db.query(Question).get(_question_vote.question_id)
    if not question:
        raise HTTPException(
            status_code=starlette.status.HTTP_400_BAD_REQUEST,
            detail='데이터 없음'
        )
    question.voter.append(current_user)
    db.add(question)
    db.commit()


@router.put('/update', status_code=starlette.status.HTTP_204_NO_CONTENT)
def question_modify(_question_modify:question_schema.QuestionModify,
                    current_user:User=Depends(get_current_user),
                    db:Session=Depends(get_db)):
    question_id = _question_modify.question_id
    subject = _question_modify.subject
    content = _question_modify.content
    question = db.query(Question).filter(Question.id==question_id).first()
    if not question:    
        raise HTTPException(
            status_code=starlette.status.HTTP_400_BAD_REQUEST,
            detail="데이터 없음"
        )
    #권한검사
    if current_user.id != question.user.id:
        raise HTTPException(
            status_code=starlette.status.HTTP_401_UNAUTHORIZED,
            detail="수정권한 없어요~"
        )
    question.subject = subject #update
    question.content = content #update
    question.modify_date = datetime.now()
    db.add(question)
    db.commit()    


@router.post('/create', status_code=starlette.status.HTTP_204_NO_CONTENT)
def question_create(_question_create:question_schema.QuestionCreate,
                    current_user:User=Depends(get_current_user),
                    db:Session=Depends(get_db)):
    subject = _question_create.subject
    content = _question_create.content
    print(subject, content)
    question = Question(
        subject=subject,
        content=content,
        create_date=datetime.now(),
        user=current_user
    )    
    db.add(question)
    db.commit()
    

@router.get('/detail/{question_id}', response_model=question_schema.Question)
def question_detail(question_id:int,
                    db:Session=Depends(get_db)):
    question = db.query(Question).get(question_id)
    answers = question.question_answers
    print(len(answers))
    return question


@router.get('/list', response_model=list[question_schema.Question])
def question_list(kw:str='',
                  db:Session=Depends(get_db)):
    question_list = db.query(Question)
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.query(Answer.question_id, Answer.content, User.username).outerjoin(User, (Answer.user_id == User.id)).subquery()
        question_list = question_list.outerjoin(User).outerjoin(sub_query, (sub_query.c.question_id == Question.id)).filter(Question.subject.ilike(search) | # 질문제목
            Question.content.ilike(search) |        # 질문내용
            User.username.ilike(search) |           # 질문작성자
            sub_query.c.content.ilike(search) |     # 답변내용
            sub_query.c.username.ilike(search)      # 답변작성자
        )
    question_list = question_list.order_by(Question.create_date.desc()).distinct().all()
    return question_list