from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./notice.db"

#커넥션
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

#db에 접근해서 CRUD할때 cursur
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#모델 구성시 상속
Base = declarative_base()

#db연동
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()