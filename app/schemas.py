from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Userout(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: Userout

    class Config:
        # orm_mode = True
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class AuthLogin(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Token(BaseModel):
    access_token: str
    token_type: str


# vote
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # conint作用，对其进行限制 le小于等于 ge大于等于 lt小于 gt大于,目前是让dir小于等于1，也可以为复数


class PostOut(BaseModel):
    Posts: Post  # 根据数据库名字来写
    votes_counts: int  # 所查询字段名

    class Config:
        # orm_mode = True
        from_attributes = True
