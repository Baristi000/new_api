from sqlalchemy.orm import Session

from models import sim,message
from schemas import sim_schema

def get_sim(db: Session, port_number: str,tty_gateway:str):
    return db.query(sim.Sim).filter(sim.Sim.port_number == port_number,sim.Sim.tty_gateway == tty_gateway).first()

def get_sim_by_number(db: Session, sim_number: str):
    return db.query(sim.Sim).filter(sim.Sim.sim_number ==sim_number ).first()


def create_sim(db: Session, created_sim: sim_schema.SimCreate):
    db_sim = sim.Sim(port_number=created_sim.port_number,tty_gateway=created_sim.tty_gateway, sim_number=created_sim.sim_number,status=created_sim.status)

    db.add(db_sim)
    db.commit()
    db.refresh(db_sim)
    return db_sim

def get_message(db:Session,sim_number:str):
    return db.query(message.Message).filter(message.Message.sim_number==sim_number).all()

def count_shop(db:Session,sim_number:str):
    return db.query(message.Message).filter(message.Message.sim_number==sim_number).count()