from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware




app = FastAPI()


#---------- CORS
origins = {
    "http://localhost:5173"
}
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#---------- router
from domain.question import question_router
from domain.user import user_router
from domain.answer import answer_router

app.include_router(question_router.router)
app.include_router(user_router.router)
app.include_router(answer_router.router)
