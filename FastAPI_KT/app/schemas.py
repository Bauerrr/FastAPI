from pydantic import BaseModel


class ContactBase(BaseModel):
    name: str
    last_name: str
    phone_number: str
    email_address: str

class Contact(ContactBase):
    contact_id: int

    class Config:
        orm_mode = True
