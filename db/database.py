from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
MYSQL_SERVER :str ="127.0.0.1"
MYSQL_PORT :int =3306
MYSQL_PASSWORD :str ="Daipro184"
MYSQL_USER:str ="root"
MYSQL_DB:str ="dai"
SQLACHEMY_CONNECTION_STRING = 'mysql+pymysql://{}:{}@{}/{}'.format(MYSQL_USER,quote_plus(MYSQL_PASSWORD), MYSQL_SERVER, MYSQL_DB)
    
SQLALCHEMY_DATABASE_URL = SQLACHEMY_CONNECTION_STRING

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()