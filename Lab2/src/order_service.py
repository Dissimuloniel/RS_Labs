from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

orders = {
    1: [{"id": 1, "item": "Laptop", "price": 999}, 
        {"id": 2, "item": "Mouse", "price": 25}],
    2: [{"id": 3, "item": "Book", "price": 15}]
}

next_order_id = 100


@app.route('/orders/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    user_orders = orders.get(user_id, [])
    return jsonify(user_orders)


@app.route('/orders', methods=['GET'])
def get_all_orders():
    return jsonify(orders)


@app.route('/orders/<int:user_id>', methods=['POST'])
def create_order(user_id):
    global next_order_id
    data = request.get_json()
    
    if not data or 'item' not in data or 'price' not in data:
        return jsonify({"error": "Item and price required"}), 400
    
    if user_id not in orders:
        orders[user_id] = []
    
    new_order = {
        "id": next_order_id,
        "item": data['item'],
        "price": data['price']
    }
    orders[user_id].append(new_order)
    next_order_id += 1
    
    return jsonify(new_order), 201


@app.route('/orders/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    # Delete order by ID across all users
    for user_id, user_orders in orders.items():
        for i, order in enumerate(user_orders):
            if order['id'] == order_id:
                deleted = user_orders.pop(i)
                return jsonify({"message": "Order deleted", "order": deleted})
    return jsonify({"error": "Order not found"}), 404


@app.route('/orders/user/<int:user_id>', methods=['DELETE'])
def delete_user_orders(user_id):
    if user_id in orders:
        del orders[user_id]
        return jsonify({"message": f"All orders for user {user_id} deleted"})
    return jsonify({"error": "User not found"}), 404


if __name__ == '__main__':
    app.run(port=5001, debug=True)