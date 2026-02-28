from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

users = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"},
    3: {"name": "Amogus", "email": "amogus.sus@example.com"},
}

next_user_id = 100

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


@app.route('/users', methods=['POST'])
def create_user():
    global next_user_id
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email required"}), 400
    
    user_id = next_user_id
    users[user_id] = {
        "name": data['name'],
        "email": data['email']
    }
    next_user_id += 1
    
    return jsonify({"id": user_id, "user": users[user_id]}), 201


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        # Optionally notify order service to delete user's orders
        try:
            requests.delete(f'http://localhost:5001/orders/user/{user_id}', timeout=2)
        except:
            pass  # Order service might be down, that's ok
        return jsonify({"message": "User deleted"})
    return jsonify({"error": "User not found"}), 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)