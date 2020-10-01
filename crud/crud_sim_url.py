from sqlalchemy.orm import Session

from models import sim_url

def create_new_sim_url(db: Session, sim_number:str,url_id:str):
    db_sim_url = sim_url.Sim_Url(sim_number=sim_number,url=url_id)
    db.add(db_sim_url)
    db.commit()
    db.refresh(db_sim_url)
    return db_sim_url

def get_sim_url(db:Session,sim_number:str,url_id:str):
    return db.query(sim_url.Sim_Url).filter(sim_url.Sim_Url.sim_number==sim_number,sim_url.Sim_Url.url==url_id).all()
    

def count_sim_of_url(db:Session,url_id:str):
    return db.query(sim_url.Sim_Url).filter(sim_url.Sim_Url.url==url_id).count()
    

