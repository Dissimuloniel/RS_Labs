from flask import Flask, jsonify

app = Flask(__name__)

# In-memory placeholder instead of DB
orders = {
    1: [{"id": 101, "item": "Laptop", "price": 999}, 
        {"id": 102, "item": "Mouse", "price": 25}],
    2: [{"id": 103, "item": "Book", "price": 15}]
}

@app.route('/orders/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    user_orders = orders.get(user_id, [])
    return jsonify(user_orders)

@app.route('/orders', methods=['GET'])
def get_all_orders():
    return jsonify(orders)

if __name__ == '__main__':
    app.run(port=5001, debug=True)