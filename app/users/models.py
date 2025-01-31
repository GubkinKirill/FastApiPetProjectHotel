from sqlalchemy import Column, Computed, Date, ForeignKey, Integer, String
from app.database import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hached_password = Column(String, nullable=False)