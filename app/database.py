import sys
sys.path.append("E:/code/company_project/fast_api/fastapi_my")
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="142511",
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as e:
#         print("Database to database failed")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
