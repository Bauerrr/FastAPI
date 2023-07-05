from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def read_contact(db: Session, contact_id: int):
    """Read operation for getting one contact by id"""
    return db.query(models.Contact).filter(models.Contact.contact_id == contact_id).first()

def read_contacts(db: Session):
    """Read operation for getting all contacts in the database"""
    return db.query(models.Contact).all()

def read_contact_by_name_and_last_name(db: Session, name: str, last_name: str):
    """Read operation for getting contact by its name and last_name"""
    return db.query(models.Contact).filter((models.Contact.name == name) & (models.Contact.last_name == last_name)).all()

def read_contact_by_name(db: Session, name: str):
    """Read operation for getting contact by its name"""
    return db.query(models.Contact).filter(models.Contact.name == name).all()

def read_contact_by_last_name(db: Session, last_name: str):
    """Read operation for getting contact by its last_name"""
    return db.query(models.Contact).filter(models.Contact.last_name == last_name).all()

def read_contact_by_email(db: Session, email: str):
    """Read operation for getting contact by its email"""
    return db.query(models.Contact).filter(models.Contact.email_address == email).all()

def read_contact_by_phone_number(db: Session, phone_number: str):
    return db.query(models.Contact).filter(models.Contact.phone_number == phone_number).all()

def create_contact(db: Session, contact: schemas.ContactBase):
    """Create operation for creating single contact"""
    db_contact = models.Contact(name=contact.name, last_name=contact.last_name, phone_number=contact.phone_number, email_address=contact.email_address)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, update_data: dict, contact_id: int):
    """Update operation for updating single contact properties"""
    db.query(models.Contact).filter(models.Contact.contact_id == contact_id).update(update_data)
    db.commit()
    return db.query(models.Contact).filter(models.Contact.contact_id == contact_id).first()

def delete_contact(db: Session, contact_id: int):
    db.query(models.Contact).filter(models.Contact.contact_id == contact_id).delete()
    db.commit()
    
def read_user(db: Session, username: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    return db_user

def create_user(db: Session, user: schemas.User):
    db_user = models.User(username=user.username, password=pwd_context.hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user