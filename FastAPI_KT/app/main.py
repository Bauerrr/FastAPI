from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# TODO: gety za pomocą query elements imie i nazwisko

@app.get("/")
def get_hello():
    endpoints ={
        "/contacts/": "get all contacts in database"
    }
    return endpoints

@app.get("/contacts/", response_model=list[schemas.Contact])
def get_contacts(db: Session = Depends(get_db)):
    """Return all contacts in database"""
    contacts = crud.read_contacts(db=db)
    return contacts

@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """Return contact with given id"""
    db_contact = crud.read_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactBase, db: Session = Depends(get_db)):
    """Check if contact with given phone number exists in database, if not create contact"""
    db_contact = crud.read_contact_by_phone_number(db=db, phone_number=contact.phone_number)
    if db_contact:
        raise HTTPException(status_code=400, detail="Contact already exists")
    return crud.create_contact(db=db, contact=contact)

@app.patch("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, update_data: dict, db: Session = Depends(get_db)):
    """Update contact with given id an values to change"""
    db_contact = crud.read_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return crud.update_contact(db=db, update_data=update_data, contact_id=contact_id)

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.read_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return crud.delete_contact(db=db, contact_id=contact_id)