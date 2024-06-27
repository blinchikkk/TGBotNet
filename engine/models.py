from sqlalchemy import Column, Integer, String, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    app_id = Column(BigInteger, nullable=False)
    hash_id = Column(String, nullable=False)
    username = Column(String)
    user_id = Column(BigInteger)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)
