from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.orm import sessionmaker
from db.base_class import Base

class Url(Base):
    __tablename__ = "url" 
    id = Column(Integer,primary_key=True, autoincrement=True)  
    url = Column(String(45)) 
