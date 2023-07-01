from sqlalchemy import Column, Integer, String

from .database import Base

class Contact(Base):
    __tablename__ = "contacts"

    contact_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    email_address = Column(String)