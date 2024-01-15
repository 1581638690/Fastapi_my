from fastapi import FastAPI
# import sys
from fastapi.middleware.cors import CORSMiddleware


# sys.path.append("E:\\code\\company_project\\fast_api\\fastapi_my\\app")
import models
from database import engine
from routers import post, user, auth,vote

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

my_post = [
    {"title": "黄金海岸", "content": "美丽海滩", "id": 1},
    {"title": "弗洛里亚", "content": "最真实的写照", "id": 2}
]

origins = [
    "*"


]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)