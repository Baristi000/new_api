from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.orm import sessionmaker
from db.base_class import Base

class Sim_Url(Base):
    __tablename__ = "sim_url" 
    sim_number = Column(String(45),primary_key=True)  
    url = Column(String(45),primary_key=True) 
