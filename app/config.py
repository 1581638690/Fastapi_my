import sys
sys.path.append("E:/code/company_project/fast_api/fastapi_my")
# 为了提高程序中隐私代码的保密性，需要将一些配置项做隐蔽处理
from pydantic_settings import BaseSettings


# from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = "E:\\code\\company_project\\fast_api\\fastapi_my\\app\\.env"
        env_file_encoding = "utf-8"


settings = Settings()