from flask import Flask, render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__)

USER_SERVICE = 'http://localhost:5000'
ORDER_SERVICE = 'http://localhost:5001'

@app.route('/')
def index():
    # Get all users
    try:
        users_response = requests.get(f'{USER_SERVICE}/users', timeout=3)
        users = users_response.json() if users_response.status_code == 200 else {}
    except:
        users = {}
    
    # Get all orders
    try:
        orders_response = requests.get(f'{ORDER_SERVICE}/orders', timeout=3)
        orders = orders_response.json() if orders_response.status_code == 200 else {}
    except:
        orders = {}
    
    return render_template('index.html', users=users, orders=orders)

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    email = request.form.get('email')
    
    if name and email:
        try:
            requests.post(f'{USER_SERVICE}/users', 
                         json={'name': name, 'email': email},
                         timeout=3)
        except:
            pass
    
    return redirect(url_for('index'))

@app.route('/add_order', methods=['POST'])
def add_order():
    user_id = request.form.get('user_id')
    item = request.form.get('item')
    price = request.form.get('price')
    
    if user_id and item and price:
        try:
            requests.post(f'{ORDER_SERVICE}/orders/{user_id}', 
                         json={'item': item, 'price': float(price)},
                         timeout=3)
        except:
            pass
    
    return redirect(url_for('index'))

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    try:
        requests.delete(f'{USER_SERVICE}/users/{user_id}', timeout=3)
    except:
        pass
    return redirect(url_for('index'))

@app.route('/delete_order/<int:order_id>')
def delete_order(order_id):
    try:
        requests.delete(f'{ORDER_SERVICE}/orders/order/{order_id}', timeout=3)
    except:
        pass
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5002, debug=True)