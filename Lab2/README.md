# Running
install `flask` and `requests` via pip

Terminal A: `python3 user_service.py`\
Terminal B: `python3 order_service.py`\
Terminal C: `python3 web_app.py` WIP

# API calls
#### Get all users: 
http://localhost:5000/users
    
#### Get all orders
http://localhost:5001/orders

#### Get specific user with orders (user service calls order service):
http://localhost:5000/users/1 where 1 is a user id

#### Get all orders from user:
http://localhost:5001/orders/1 where 1 is a user id