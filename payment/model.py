from sqlalchemy import Column, Integer, String,Float
from .database import Base

#model
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    fee = Column(Float)
    total = Column(Float)
    quantity = Column(Integer)
    status = Column(String)
    product_id = Column(Integer)