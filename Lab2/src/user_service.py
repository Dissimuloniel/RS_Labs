from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

users = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"},
    3: {"name": "Amogus", "email": "amogus.sus@example.com"},
}

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    
    if not user:
        return jsonify({"Error": "User not found"}), 404
    
    # fetching orders
    try:
        orders_response = requests.get(f'http://localhost:5001/orders/{user_id}')
        if orders_response.status_code == 200:
            user['orders'] = orders_response.json()
    except:
        return jsonify({"Error": "Fetching orders failed!"}), 404
        
    return jsonify(user)

if __name__ == '__main__':
    app.run(port=5000, debug=True)