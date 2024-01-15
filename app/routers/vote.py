from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
# import sys

# sys.path.append("E:\\code\\company_project\\fast_api\\fastapi_my\\app")
import models
import database
import oauth2
from schemas import *

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: Vote, db: Session = Depends(database.get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    # 首先进行访问不存在的数据返回404
    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Vote {vote.post_id} does not exist!")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id,
                                               models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        # 先判断存不存在
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has alredy voted on post {vote.post_id}")
        # 不存在该，则进行存储
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"mssage": "successfully added vote!"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        vote_query.delete()
        db.commit()
        return {"mssage": "successfully removed vote!"}
