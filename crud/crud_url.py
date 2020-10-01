from sqlalchemy.orm import Session

from models import url
from crud import crud_sim_url
def create_new_url(db: Session, new_url:str):
    db_url = url.Url(url=new_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_url(db:Session,id:str):
    return db.query(url.Url).filter(url.Url.id==id).all()


def get_all_url(db:Session):
    urls= db.query(url.Url).all()
    for u in urls:
        u.number_of_sim=crud_sim_url.count_sim_of_url(db=db,url_id=u.id)
    return urls


def update_url(db:Session,id:str,new_url:str):
    db.query(url.Url).filter(url.Url.id==id).update({url.Url.url: new_url})
    db.commit()