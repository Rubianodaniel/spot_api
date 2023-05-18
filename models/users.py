from config.db import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class UsersModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    disable = Column(Boolean, nullable= True)
    password_id = Column(Integer, ForeignKey("passwords.id"))
    password = relationship("PasswordModel", uselist=False, backref="user")

 
class PasswordModel(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String, nullable=False)


