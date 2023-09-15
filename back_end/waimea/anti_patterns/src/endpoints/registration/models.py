import uuid
from sql.models.base import Base
from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy_utils import force_auto_coercion


force_auto_coercion()

class Customers(Base):

    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    uuid = Column(String(36), default=lambda x: str(uuid.uuid4()))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
