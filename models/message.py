
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.orm import sessionmaker
from db.database import Base

class Message(Base):
    __tablename__ = "message"
    id = Column(String(45), primary_key=True)
    sim_number = Column(String(45))  
    otp = Column(String(45))  
    raw_message = Column(String(200))  
    time_stamp = Column(String(45))  
    shop_id = Column(String(45))   

