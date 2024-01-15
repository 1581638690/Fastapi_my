from datetime import datetime, timedelta
from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config import Settings
settings = Settings()
# import sys
# sys.path.append("E:\\code\\company_project\\fast_api\\fastapi_my\\app")
import schemas
import models
from database import *
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# 创建密钥
SECRET_KEY = f"{settings.secret_key}"
# 创建指定JWT令牌签名算法的变量
ALGORITHM = f"{settings.algorithm}"
# 创建设置令牌过期时间的变量
ACCESS_TOKEN_EXPIRE_MINUTES =settings.access_token_expire_minutes


# jwt 组成接口，secret_key 密钥, expires_delta 过期时间,加密方法
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def verify_access_token(token: str, creadentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise creadentials_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise creadentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                          detail=f'Could not validate credentials',
                                          headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    return user
