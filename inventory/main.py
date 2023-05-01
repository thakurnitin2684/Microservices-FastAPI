from fastapi import FastAPI
from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from redis_om import get_redis_connection, HashModel
from sqlalchemy import Column, Integer, String, ForeignKey
from .database import SessionLocal,engine,Base,get_db
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import event

if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "examples"

from payment.model import Order

app = FastAPI(title="Inventory", version="1.0.0",)
#model
session=SessionLocal(bind=engine)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)

#schema
class ProductSchema(BaseModel):
    name:str
    price:int
    quantity : int
    class Config():
        orm_mode = True
Base.metadata.create_all(engine)


##for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

# redis = get_redis_connection(
#     host="redis-11844.c135.eu-central-1-1.ec2.cloud.redislabs.com",
#     port=11844,
#     password="pRdcpRkKPFn6UnEFskrDGxrmFbf5T9ER",
#     decode_responses=True
# )



@app.get('/products')
def all(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return [format(i) for i in products]
    # return blogs

def format(product: Product):
    return {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.post('/products')
def create(product: ProductSchema,db: Session = Depends(get_db)):
    new_product = Product(name=product.name, price=product.price, quantity= product.quantity)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get('/products/{id}',status_code=200)
def get(id: int,db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with the id {id} is not available")
    return product


@app.delete('/products/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int,db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id)

    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id {id} not found")

    product.delete(synchronize_session=False)
    db.commit()
    return 'done'

 
@event.listens_for(Order, "before_insert")
def lowercase(mapper, connection, target):
    product = session.query(Product).filter(Product.id == target.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with the id {target.product_id} is not available")
    product.quantity=product.quantity-target.quantity
    session.commit()
