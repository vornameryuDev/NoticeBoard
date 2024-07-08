from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, null
from sqlalchemy.orm import relationship
from database import Base



question_voter = Table(
    'question_voter',
    Base.metadata,
    Column('question_id', Integer, ForeignKey('question.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True)
)
answer_voter = Table(
    'answer_voter',
    Base.metadata,
    Column('answer_id', Integer, ForeignKey('answer.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True) #pk
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    create_date = Column(DateTime, nullable=False)


class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True) #pk
    subject = Column(String, nullable=False)
    content = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id')) #fk=user
    user = relationship('User', backref='questions') #backref
    modify_date = Column(DateTime, nullable=True)
    voter = relationship('User', secondary='question_voter', backref='question_voter')


class Answer(Base):
    __tablename__ = 'answer'
    id = Column(Integer, primary_key=True) #pk
    content = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id')) #fk=user
    user = relationship('User', backref='user_answers') #backref=user
    question_id = Column(Integer, ForeignKey('question.id')) #fk=question
    question = relationship('Question', backref='question_answers') #backref=question
    modify_date = Column(DateTime, nullable=True)
    voter = relationship('User', secondary='answer_voter', backref='answer_voter')
