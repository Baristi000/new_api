from sqlalchemy.orm import Session

from models import country
from schemas import country_schema

def get_country(db: Session, country_id: str):
    return db.query(country.Country).filter(country.Country.postl_code == country_id).first()

def get_all_country(db: Session):
    return db.query(country.Country).all()

