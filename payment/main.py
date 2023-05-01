from fastapi import FastAPI
from fastapi import Depends,status,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks

from sqlalchemy import Column, Integer, String,Float
from .database import Base,engine,get_db
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .model import Order
import requests,time 

if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "examples"

from inventory.main import session,Product


app = FastAPI(title="Payment", version="1.0.0",)



#schema
class OrderSchema(BaseModel):
    id : int
    quantity : int
    class Config():
        orm_mode = True


Base.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)






@app.get('/orders/{pk}',status_code=200)
def get(id: int,db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"order with the id {id} is not available")
    return order 
 




@app.post('/orders')
async def create(od: OrderSchema, background_tasks: BackgroundTasks,db: Session = Depends(get_db)):  # id, quantity
    print(od)
    req = requests.get('http://localhost:8000/products/%s' % od.id)
    product = req.json()

    order = Order(
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=od.quantity,
        status='pending',
        product_id= od.id
    )
    
    db.add(order)
    db.commit()
    db.refresh(order)
    background_tasks.add_task(order_completed, order,db)
    return order


def order_completed(order: Order,db: Session = Depends(get_db),):
    time.sleep(5)
    order.status = 'completed'
    db.commit()
    db.refresh(order)

    # product = session.query(Product).filter(Product.id == order.product_id).first()
    # if not product:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Product with the id {order.product_id} is not available")
    # product.quantity=product.quantity-order.quantity
    # session.commit()
    # redis.xadd('order_completed', order.dict(), '*')

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port= '8001')

