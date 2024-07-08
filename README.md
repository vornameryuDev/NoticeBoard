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


### 2. API정의
|번호|api|detail|method|return|
|:--:|:--|:--|:--|:--|
|1|/api/question/|list|get|[]|
|2||detail/{question_id}|get|{}|
|3||create|post|204|
|4||update|put|204|
|5||delete|delete|204|
|6||vote|post|204|
|1|/api/user/|login|post|204|
|2||create|post|204|
|1|/api/answer/|create|post|204|
|2||detail/{answer_id}|get|{}|
|3||update|put|204|
|4||vote|post|204|
|5||delete|delete|204|


### 3. 모델
````
1. User
  - tablename: user
  - columns: id, username, password, email, create_date
  
2. Question
  - tablename: question
  - columns: id, subject, content, create_date, user_id, user, modify_date, voter

3. Answer
  - tablename: answer
  - columns: id, content, create_date, user_id, user, modify_date, voter

4. question_voter
  - tablename: question_voter
  - columns: question_id, user_id

5. answer_voter
  - tablename: answer_voter
  - columns: answer_id, user_id
````

### 4. 화면

### 5. 디렉토리
````
📦noticeBoard
 ┣ 📂backend
 ┃ ┣ 📂domain
 ┃ ┃ ┣ 📂answer
 ┃ ┃ ┃ ┣ 📜answer_router.py
 ┃ ┃ ┃ ┗ 📜answer_schema.py
 ┃ ┃ ┣ 📂question
 ┃ ┃ ┃ ┣ 📜question_router.py
 ┃ ┃ ┃ ┗ 📜question_schema.py
 ┃ ┃ ┗ 📂user
 ┃ ┃ ┃ ┣ 📜user_router.py
 ┃ ┃ ┃ ┗ 📜user_schema.py
 ┃ ┣ 📂migrations
 ┃ ┃ ┣ 📂versions
 ┃ ┃ ┃ ┣ 📜0112b8127bb6_.py
 ┃ ┃ ┃ ┣ 📜318458bc5fa9_.py
 ┃ ┃ ┃ ┣ 📜4cce96213d30_.py
 ┃ ┃ ┃ ┣ 📜5b7738a07b98_.py
 ┃ ┃ ┃ ┣ 📜b649f9c5daba_.py
 ┃ ┃ ┃ ┗ 📜c036f781ac83_.py
 ┃ ┃ ┣ 📜env.py
 ┃ ┃ ┣ 📜README
 ┃ ┃ ┗ 📜script.py.mako
 ┃ ┣ 📜alembic.ini
 ┃ ┣ 📜database.py
 ┃ ┣ 📜main.py
 ┃ ┣ 📜models.py
 ┃ ┗ 📜notice.db
 ┣ 📂frontend
 ┃ ┣ 📂components
 ┃ ┃ ┣ 📜Error.svelte
 ┃ ┃ ┗ 📜Navigation.svelte
 ┃ ┣ 📂routes
 ┃ ┃ ┣ 📜AnswerModify.svelte
 ┃ ┃ ┣ 📜Detail.svelte
 ┃ ┃ ┣ 📜Home.svelte
 ┃ ┃ ┣ 📜QuestionCreate.svelte
 ┃ ┃ ┣ 📜QuestionModify.svelte
 ┃ ┃ ┣ 📜UserCreate.svelte
 ┃ ┃ ┗ 📜UserLogin.svelte
 ┃ ┣ 📂src
 ┃ ┃ ┣ 📂assets
 ┃ ┃ ┣ 📂lib
 ┃ ┃ ┃ ┣ 📜api.js
 ┃ ┃ ┃ ┣ 📜Detail.js
 ┃ ┃ ┃ ┗ 📜store.js
 ┃ ┃ ┣ 📜app.css
 ┃ ┃ ┣ 📜App.svelte
 ┃ ┃ ┣ 📜main.js
 ┃ ┃ ┗ 📜vite-env.d.ts
 ┃ ┣ 📜.gitignore
 ┃ ┣ 📜index.html
 ┃ ┣ 📜jsconfig.json
 ┃ ┣ 📜package-lock.json
 ┃ ┣ 📜package.json
 ┃ ┣ 📜README.md
 ┃ ┣ 📜svelte.config.js
 ┃ ┗ 📜vite.config.js
 ┗ 📜requirements.txt
````
