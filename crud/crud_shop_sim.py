from sqlalchemy.orm import Session

from models import shop_sim
from schemas import shop_sim_schema

def create_new_shop_executor(db: Session, shop_id:str,sim_number:str):
    db_shop_sim = shop_sim.Shop_sim(shop_id=shop_id,sim_number=sim_number)
    db.add(db_shop_sim)
    db.commit()
    db.refresh(db_shop_sim)
    return db_shop_sim

def get_all_shop_sim(db:Session,shop_id:str):
    return db.query(shop_sim.Shop_sim.sim_number).filter(shop_sim.Shop_sim.shop_id ==shop_id).all()

def get_all_shop_of_sim(db:Session,sim_number:str):
    return db.query(shop_sim.Shop_sim.shop_id).filter(shop_sim.Shop_sim.sim_number ==sim_number).all()


def count_shop_sim(db:Session,sim_number:str):
    return db.query(shop_sim.Shop_sim.sim_number).filter(shop_sim.Shop_sim.sim_number ==sim_number).count()