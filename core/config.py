import secrets
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator
from urllib.parse import quote_plus

class Settings(BaseSettings):
    MYSQL_SERVER :str ="127.0.0.1"
    MYSQL_PORT :int =3306
    MYSQL_PASSWORD :str ="Daipro184"
    MYSQL_USER:str ="root"
    MYSQL_DB:str ="dai"
    SQLACHEMY_CONNECTION_STRING = 'mysql+pymysql://{}:{}@{}/{}'.format(MYSQL_USER,quote_plus(MYSQL_PASSWORD), MYSQL_SERVER, MYSQL_DB)
    
    REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    SECRET_KEY:str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM:str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 1000

    scopes={
        "read_user":"view all user and user detail",
        "read_shop":"view all shop and shop detail",
        "read_channel":"view all channel and channel detail",
        "read_country":"view all country and country detail",
        "channel_manager":"update channel manager",
        "shop_executor":"update shop executor",
        "shop_sim":"update shop sim",
        "inactivate_user":"in activate user"
    }
    #test
    NEWUSER_SCOPESS=[
        "me",
        "read_user",
        "read_shop",
        "read_channel",
        "read_country",
        "read_sim"
        ]
    EXECUTOR_SCOPESS=[
        "me",
        "read_user",
        "read_shop",
        "read_channel",
        "read_country",
        "read_sim",
        "shop_sim"
        ]
    MANAGER_SCOPESS=[
        "me",
        "read_user",
        "read_shop",
        "read_channel",
        "read_country",
        "read_sim",
        "shop_sim",
        "shop_executor",
        ]
    ADMIN_SCOPESS=[
        "me",
        "read_user",
        "read_shop",
        "read_channel",
        "read_country",
        "read_sim",
        "channel_manager",
        "shop_executor",
        "shop_sim",
        "inactivate_user"
    ]
    class Config:
        case_sensitive = True
settings = Settings()