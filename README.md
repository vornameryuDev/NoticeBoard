# Notice Board

### 1.개요
````
1) Language: python(3.10.11)
2) Framework
  - Backend: FastAPI(0.111.0)
  - Forntend: Svelte(4.2.18)
3) Package / Library...
  - Backend
    - 프론트와 연결: starlette.middleware.cors.CORSMiddleware
    - 라우팅 경로 등록: fastapi.APIRouter
    - 참조함수: fastapi.Depends
    - Database
      - 커넥션 관리: sqlalchemy.create_engine
      - cursor: sqlalchemy.orm.sessionmaker, sqlalchemy.orm.Session
      - db상속: sqlalchemy.ext.declarative.declarative_base
    - schema
      - 메타정의: pydantic.BaseModel
      - 필드 유효성검사: pydantic.field_validator
    - 비밀번호 및 토큰화
      - 비밀번호 해시화: passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")
      - 토큰생성 및 비교
        - fastapi.security.OAuth2PasswordRequestForm
        - jose.jwt.encode()
        - fastapi.security.OAuth2PasswordBearer
      - 토큰해독: jose.jwt.decode()
  - Frontend
    - 라우팅: svelte-spa-router
      - push, link
    - 스토어: svelte-store
      - writable, get
    - bootstrap: booptstrap
````
