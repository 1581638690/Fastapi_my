from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Annotated, List
# import sys
from sqlalchemy.orm import Session
# sys.path.append("E:\\code\\company_project\\fast_api\\fastapi_my\\app")
import models
from database import engine, get_db
from schemas import *
from utils import *

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 创建新用户
    hash_password = pwd_context.hash(user.password)
    user.password = hash_password
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=Userout)
def get_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id).first()
    # result = user_query.first()
    if not user_query:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Found {id} Not exists!".format(id))

    return user_query
