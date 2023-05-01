## Microservices-Fast-API
This is a API for a Pizza delivery service built for fun and learning with FastAPI, SQLAlchemy and SQLite. 


## How to run the Project
- Install Python
- Git clone the project with ``` git clone https://github.com/jod35/Pizza-Delivery-API.git```
- Create your virtualenv with `Pipenv` or `virtualenv` and activate it.
- Install the requirements with ``` pip install -r requirements.txt ```

### After that
 - <strong> Run inventory on port no. 8000 </strong>
 - uvicorn inventory.main:app --reload
 
 - <strong> Run payment on portno. 8001 </strong>
 - uvicorn payment.main:app --reload
 
 - <strong> Then run react app </strong>
 - npm start
 
## ROUTES TO IMPLEMENT  "INVENTORY" 
| METHOD | ROUTE | FUNCTIONALITY |
| ------- | ----- | ------------- | 
| *GET* | ```/products``` | _Get all products_|
| *POST* | ```/products``` | _Post a new product_|
| *GET* | ```/products/{id}``` | _Get a product by id_|
| *DELETE* | ```/products/{id}``` | _Delete a product_|


## ROUTES TO IMPLEMENT "PAYMENT"
| METHOD | ROUTE | FUNCTIONALITY |
| ------- | ----- | ------------- | 
| *GET* | ```/orders/{id}``` | _Get all orders_|
| *POST* | ```/orders``` | _Post a new order_|


## UI Shots
- <strong> localhost:8000/docs </strong>
<img src="/ss/inventory.PNG">

- <strong> localhost:8001/docs </strong>
<img src="/ss/payment.PNG">

- <strong> React Front-End </strong>
<img src="/ss/ui1.PNG">
<img src="/ss/ui2.PNG">
<img src="/ss/ui3.PNG">



