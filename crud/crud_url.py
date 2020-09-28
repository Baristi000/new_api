from sqlalchemy.orm import Session

from models import url

def create_new_url(db: Session, new_url:str):
    db_url = url.Url(url=new_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_url(db:Session,id:str):
    return db.query(url.Url).filter(url.Url.id==id).all()

def update_url(db:Session,id:str,new_url:str):
    db.query(url.Url).filter(url.Url.id==id).update({url.Url.url: new_url})
    db.commit()