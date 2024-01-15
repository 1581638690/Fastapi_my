from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# import sys
# 
# sys.path.append("E:\\code\\company_project\\fast_api\\fastapi_my\\app")
import models
import utils
import database
import oauth2

# import models
# import utils
# import database
# import oauth2

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login")
# 第一种写法直接将用户名密码写入数据中
# def login(user_credentials: schemas.AuthLogin, db: Session = Depends(database.get_db)):

# 第二种方法 使用Oauth2PasswordRequestForm写入
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # 第一种方法
    # user_query = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    # 第二种方法
    user_query = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()  # 传参就必须用 form-data了
    if not user_query:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not utils.verify(user_credentials.password, user_query.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    # created a token
    # return token
    access_token = oauth2.create_access_token(data={"user_id": user_query.id})
    return {"access_token": access_token, "token_type": "beaer"}
