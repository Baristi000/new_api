from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from models import message
from fastapi import Depends
from api import deps
from db.database import SessionLocal

def get_all_message(db:Session):
    return db.query(message.Message).all()

def get_all_sim_messages(db:Session,sim_number:str):
    return db.query(message.Message).filter(message.Message.phone_owner).all()

def create_messages(db:Session,
                    phone_owner:str,
                    time:str,
                    otp:str,
                    raw_message:str,
                    from_number:str,
                    date:str,
                    shop_id:str
):
    created_messages=message.Message(phone_owner=phone_owner,
                                    time=time,
                                    otp=otp,
                                    raw_message=raw_message,
                                    from_number=from_number,
                                    date=date,
                                    shop_id=shop_id)
    db.add(created_messages)
    db.commit()
    db.refresh(created_messages)
    return created_messages
