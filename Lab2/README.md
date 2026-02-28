# Running
install `flask` and `requests` via pip

Terminal A: `python3 user_service.py`\
Terminal B: `python3 order_service.py`\
Terminal C: `python3 web_app.py` WIP

# Users service API calls examples
#### Get all users: 
`curl -i -X GET http://localhost:5000/users`

#### Get specific user with orders (user service calls order service):
`curl -i -X GET http://localhost:5000/users/1` where `1` is an user id

#### Delete user:
`curl -i -X DELETE http://localhost:5000/users/3` where `3` is an user id
    
#### Add user:
`curl -i -X POST -H 'Content-Type: application/json' -d '{"name": "Charlie", "email": "charlie@example.com"}' http://localhost:5000/users`

# Orders service API calls examples
#### Get all orders
`curl -i -X GET http://localhost:5001/orders`

#### Get all orders from user:
`curl -i -X GET http://localhost:5001/orders/1` where `1` is an user id

#### Delete order:
`curl -i -X DELETE http://localhost:5001/orders/order/3` where `3` is an order id

#### Delete order for specific user:
`curl -i -X DELETE http://localhost:5001/orders/user/3` where `3` is an user id
    
#### Add order:
`curl -i -X POST -H 'Content-Type: application/json' -d '{"item": "Keyboard", "price": 75}' http://localhost:5001/orders/1` where `1` is an user id