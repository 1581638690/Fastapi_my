# 无法关闭终端uvicorn程序步骤
1. 查询所开启的端口号：netstat -ano | find "8001"
2. 关闭并杀死该端口号：taskkill /F /PID 进程id
# 安装postgres数据库
启动：搜索 pgadmin,启动
安装依赖库：pip install psycopg2
pip install python-jose[cryptography]
pip install passlib[bcrypt]

# 生成JWT 令牌密钥
openssl rand -hex 32

# 1.fastapi连接postgres
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#创建数据库连接  "postgresql://user:password@hostname:port/dbname"
SQLALCHEMY_DATABASE_URL='postgresql://postgres:142511@localhost/fastapi'
# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 创建数据库会话
SessionLocal=sessionmaker(autocommit=False,autoflush=False, bind=engine)

# 创建数据库模型基类
Base =declarative_base()

#生成数据库连接函数
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
# 2.创建数据库表
```python
#导入需要的字段类型
from sqlalchemy import Column, INT, String, BOOLEAN, Integer, DateTime, TIMESTAMP,text
from database import Base
import datetime
#建表  示例
class User(Base): #映射的数据库表名
    __tablename__ = "users" #数据库表名
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=True,server_default=text('now()'))
```
# 3.创建视图函数统一标准路由路径
```python
#第一种情况：将路由路径写入到 main.py函数中
#第二种情况：比较规范化，将路径路由，每个api单独放进文件夹中 router文件夹中下面存在视图文件，例如auth.py
#在auth.py中
from fastapi import APIRouter, Depends
#这样配置路由
router = APIRouter(
    prefix="/login",
    tags=["login"],
    dependencies=[Depends(get_db)],
    responses={
        404: {"description":"Not Found"},
        403: {"description":"Forbidden"},
        422: {"description":"Validation Error"}
    }
)
#参数所表现意思
"""
prefix:设置路由器中所有路由得前缀，例如 prefix="/login",那么在该文件下面得所有路径都需要以/login为前提
tags:为路由器中敌营得所有路由设置标签，让路由在文档中显示得比较规范化
dependencies:设置路由器中所有路由得依赖，例如dependencies=[Depends(get_db)]，那么在路由中所有请求都需要先执行,比如认证
responses:配置默认的状态码，模型，描述
"""

# 在main.py文件中
from routers import auth
app=FastAPI()
app.include_router(auth.router)
```

# 4.创建视图函数，利用进行登录认证行为
```python
#导入fastapi中自带Oauth2认证表单
from fastapi.security import OAuth2PasswordRequestForm
@router.post("/login")
#定义路由，定义视图用来作用登录的判断逻辑
def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db):
    user_query=db.query(models.User).filter(
        models.User.email == user_credentials.username   
    ).first()
    #先判断账户是否正确，如果不正确
    if not user_query:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    #在判断密码错误
    if not utils.verify(user_credentials.password,user_query.password):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    access_token = oauth2.create_access_token(data={"user_id":user_query.id})
    return {"access_token":access_token,"token_type":"beaer"}
```

# 5.创建认证逻辑密码判断 
```python
from passlib.context import CryptContext
#创建CrypContext实例，配置 密码哈希算法的类型，auto表示当前版本如果可用，则自动弃用老版本算法
pwd_context=CryptContext(schemes=["bcrypt"],deprecated='auto')
#对密码进行hash
def hash(password:str):
    return pwd_context.hash(password)

#验证密码明文密码与hash密码是否相同
def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
```

# 6.Token验证，生成jwt
```python
from jose import JWTError,jwt
#创建密钥
SECRET_KEY='2247431704d7bb125e492f1e986cf8466e63e1bcc9ad2b281f6845c0df738f3a'
#创建指定JWT令牌签名算法的变量
ALGORITHM = "HS256"
#创建设置令牌过期时间的变量
ACCESS_TOKEN_EXPIRE_MINUTES = 60 

#创建生成jwt接口
def create_access_token(data:dict):
    to_encode=data.copy()
    expire= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    endcode_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return endcode_jwt

#然后在登录login的时候，需要生成token 并返回
```

# 7.验证token，并让某些api需要携带token才能做操作，例如 post.py
```python
#定义路径
@router.get("/posts",response_model=List[Post])
def get_data(db:Session=Depends(get_db)):
    user_query=db.query(models.Posts).all()
    return user_query
    
# 验证token
def verify_access_token(token:str,creadentoals_exception):
    try:
        pyload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get("user_id")
        if id is None:
            raise creadentoals_exception
        token_data=TokenData(id=id)
    except JWTError:
        raise creadentoals_exception
    return token_data

# 编写错误代码
def get_current_user(token:str=Depends(oauth2_scheme),db:Session = Depenes(get_db)):
    credentials_exception =HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )
    token_data=verify_access_token(token,credentials_exception)
    user=db.query(models.User).filter(model.User.id == token_data.id).first()
    return user
```
# 8.将post.py 必须经过认证才能访问数据
```python
# 1.登录login 成功获取token信息
# 2.在post.py 验证token
def get_post(db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user):
    posts =db.query(models.Posts).all()
    return posts
# 将token传入请求头中，通过验证才能获取到当前结果
```

# 数据库迁移 alembic
```text
#1. 安装alembic
    pip install alembic
#2. 创建alembic.ini文件
    alembic init alembic
#3. 编辑alembic/env.py文件
    导入数据库Base设置
    导入我们的密码配置
    from app.database import Base
    from app.config import Settings
    
    config.set_main_option("sqlalchemy.url",Settings.database_url) #本来是sql链接是要写入到ini文件中的，由于我们的配置
    target_metadata = Base.metadata
#4.生成迁移脚本
    alembic revision -m "create account table"
#5.创建表结构
    在生成的迁移脚本中写入自己需要添加的表结构

#6.执行迁移脚本
    alembic upgrade head "" 脚本中 revision的变量号
    
# 7.查看 导出环境包
pip freeze > requirements.txt
```
