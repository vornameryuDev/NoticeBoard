from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import starlette.status
from models import User
from database import get_db
from domain.user import user_schema
from sqlalchemy.orm import Session
from passlib.context import CryptContext #비밀번호 해시화
from jose import JWTError, jwt


router = APIRouter(prefix='/api/user',)



#비밀번호 해시로 변환
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#토큰만들기
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "6e081e7a419f5a0e587bcdc2f3d583d476b3b79d8585212c1b21c636bcd257a1"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/user/login') #토큰 생성한 api


#로그인한 사람의 정보 추출(OAuth2): 토큰가져오기(디코드) > 토큰에서 사용자 정보 얻기
def get_current_user(token:str=Depends(oauth2_scheme),
                     db:Session=Depends(get_db)):
    credential_exception = HTTPException(
        status_code=starlette.status.HTTP_401_UNAUTHORIZED,
        detail='권한없음',
        headers={'WWW-Authenticate': "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #{'sub':, 'exp':}
        username: str = payload.get('sub') #사용자 이름 가져오기
        if username is None: #이름 없으면=로그인 한적 없음 > 오류발생
            raise credential_exception
    except JWTError:
        raise credential_exception
    else: #항상 실행
        user = db.query(User).filter(User.username==username).first() #db에 찾기
        if user is None: #db에 없는 정보 > 오류발생
            raise credential_exception
        return user
        



#oath2 인증사용해서 로그인 > 토큰부여 > localStorage 저장
@router.post('/login', response_model=user_schema.Token)
def user_login(form_data:OAuth2PasswordRequestForm=Depends(), #로그인 화면에서 입력되는 정보는 여기로 들어옴
               db:Session=Depends(get_db)):
    #로그인 정보 체크
    db_user = db.query(User).filter(User.username==form_data.username).first()
    if not db_user or not pwd_context.verify(form_data.password, db_user.password):
        # db에 없거나 입력한 비밀번호와 db에 저장된 비밀번호가 다를경우
        raise HTTPException(
            status_code=starlette.status.HTTP_401_UNAUTHORIZED,
            detail='뭔가 잘못입력 or 정보없음',
            headers={"WWW-Authenticate": "Bearer"}, #401에러인 경우 정보 헤더에
        )
    
    #토큰부여
    data = {
        'sub': db_user.username, #유저이름
        'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)#토큰유효기간
    }
    access_token = jwt.encode(data, key=SECRET_KEY, algorithm=ALGORITHM)
    
    #localStorage저장을 위해 access_token 리턴
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'username': db_user.username
    }


@router.post('/create', status_code=starlette.status.HTTP_204_NO_CONTENT)
def user_create(_user_create:user_schema.UserCreate,
         db:Session=Depends(get_db)):
    #username과 emal이 일치하는 경우 조회
    user = db.query(User).filter(
        User.username == _user_create.username or User.email == _user_create.username
    ).first()    
    if user:
        #일치하면 오류발생
        raise HTTPException(
            status_code=starlette.status.HTTP_409_CONFLICT,
            detail='이미 존재하는 사용자'
        )
    #일치하지 않을 경우
    db_user = User(
        username = _user_create.username,
        password = pwd_context.hash(_user_create.password1),
        email = _user_create.email,
        create_date = datetime.now()
    )
    db.add(db_user)
    db.commit()