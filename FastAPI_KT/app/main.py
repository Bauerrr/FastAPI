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
def get_contacts(db: Session = Depends(get_db), name: str | None = None, last_name: str | None = None,
                 phone_number: str | None = None, email: str | None = None):
    """Return all contacts in database. If name or last name is given as query parameters, 
        return only contacts with given (name), (last name), (name and last name).
        If email is given as query parameter, return contacts with given email.
        If phone_number is given as query parameter, return contact with given phone number. 
        If there aren't any contacts in database return empty.
        """
    if name and last_name:
        contacts = crud.read_contact_by_name_and_last_name(db=db, name=name, last_name=last_name)
    elif name:
        contacts = crud.read_contact_by_name(db=db, name=name)
    elif last_name:
        contacts = crud.read_contact_by_last_name(db=db, last_name=last_name)
    elif email:
        contacts = crud.read_contact_by_email(db=db, email=email)
    elif phone_number:
        contacts = crud.read_contact_by_phone_number(db=db, phone_number=phone_number)
    else:
        contacts = crud.read_contacts(db=db)
    return contacts

@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """Return contact with given id. If contact doesn't exist return 404 status code."""
    db_contact = crud.read_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactBase, db: Session = Depends(get_db)):
    """Check if contact with given phone number exists in database, if not create contact. If contact already exists return status code 400."""
    db_contact = crud.read_contact_by_phone_number(db=db, phone_number=contact.phone_number)
    if db_contact:
        raise HTTPException(status_code=400, detail="Contact already exists")
    return crud.create_contact(db=db, contact=contact)

@app.patch("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, update_data: dict, db: Session = Depends(get_db)):
    """Update contact with given id with values to change. If contact doesn't exist return 404 status code."""

    allowed_keys = ("name", "last_name", "phone_number", "email_addres")
    # Check if dict keys are allowed
    for i in update_data.keys():
        if i not in allowed_keys:
            raise HTTPException(status_code=422)
    
    # Raise 422 if update_data dict is empty
    if not update_data:
        raise HTTPException(status_code=422)
    
    db_contact = crud.read_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return crud.update_contact(db=db, update_data=update_data, contact_id=contact_id)

@app.delete("/contacts/{contact_id}", status_code=204)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """Delete contact with given id. If contact doesn't exist return 404 status code."""
    db_contact = crud.read_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return crud.delete_contact(db=db, contact_id=contact_id)