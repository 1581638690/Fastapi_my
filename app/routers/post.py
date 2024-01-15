from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Annotated, List, Optional
from random import randrange
# import sys
from sqlalchemy.orm import Session
from sqlalchemy import func
# sys.path.append("E:\\code\\company_project\\fast_api\\fastapi_my\\app")
import models
from database import get_db
from schemas import *
import oauth2

router = APIRouter(
    prefix="/post",
    tags=["Post"]
)


# 创建一个CURD函数 ,提供查询参数
# @router.get("/", response_model=List[PostOut])  # 由于查出所有数据是多条，所以需要将数据存放在List中
@router.get("/", response_model=List[PostOut])
def get_post(db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user),
             limit: int = 10, skip: int = 0, search: Optional[str] = ""):  # API路由之前执行的函数 Depends
    """
    :param db: 数据库连接
    :param get_current_user: 认证请求
    :param limit: 获取条数的最大限制 默认是10
    :param skip:  获取数据索引 即最小值
    :param search: 关键词，搜索数据中包含的关键词
    :return:
    """
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()
    # 找出owner_id为当前id的
    # posts = db.query(models.Posts).filter(models.Posts.owner_id == get_current_user.id)
    # posts = db.query(models.Posts).all()
    # posts = db.query(models.Posts).limit(limit).all()
    posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Posts, func.count(models.Votes.post_id).label("votes_counts")).join(
        models.Votes, models.Votes.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).filter(
        models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    print(results)
    return results


@router.post("/", response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000)
    # 使用ORM进行存储数据,第一种方法
    # new_post = models.Posts(title=post_dict.get("title"), content=post_dict.get("content"),published=post_dict.get("published"))
    # 使用ORM进行存储数据，第二种方法
    print(current_user.id)
    new_post = models.Posts(owner_id=current_user.id, **post_dict)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # 创建数据
    # query = "insert into posts (title,content,published) values (%s,%s,%s)"
    # cars = (
    #     (post_dict["title"], post_dict["content"], post_dict["published"])
    # )
    # cursor.execute("""insert INTO posts (title,content,published) VALUES (%s,%s,%s) returning *""",
    #                (post_dict["title"], post_dict["content"], post_dict["published"]))
    # cursor.executemany(query, cars)
    # conn.commit()
    # my_post.append(post_dict)
    return new_post


@router.get("/{id}", response_model=PostOut)
def get_id_data(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # data = get_id(id)
    # cursor.execute("""select * from posts where id=%s""", str(id))
    # rows = cursor.fetchall()
    rows = db.query(models.Posts, func.count(models.Votes.post_id).label("votes_counts")).join(
        models.Votes, models.Votes.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).filter(
        models.Posts.id == id).first()
    if not rows:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Not Found ID"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found ID")
    # if rows.Posts.owner_id != current_user.id:
    #     return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User mismatch!")
    return rows


@router.delete("/{id}")
def delete_id(id: int, response: Response, db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user)):
    # index = find_get_index(id)
    # cursor.execute("""delete from posts where id=%s""", str(id))
    # conn.commit()
    rows = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not rows:
        # my_post.pop(index)
        return {"msg": "index Not Found!"}

    if rows.owner_id != current_user.id:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User mismatch!")
    rows.delete(synchronize_session=False)
    db.commit()

    return {"mssage": "data successful deleted"}


@router.put("/{id}", response_model=Post)
def update_data(id: int, post: PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # 更新操作
    # post_dict = post.dict()
    # cursor.execute("""update posts set title=%s,content=%s,published=%s where id =%s returning *""",(post_dict["title"], post_dict["content"], post_dict["published"], id))
    # update_post = cursor.fetchone()
    # index = find_get_index(id)
    # conn.commit()
    # 先查出想要更新那个
    print(id)

    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    post_data = post_query.first()
    print(post_data)

    if not post_data:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Found {id} Not exists!".format(id))

    if post_data.owner_id != current_user.id:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User mismatch!")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_data
