from flask import Flask, request, jsonify
import threading
import requests
import time
from datetime import datetime
import random

app = Flask(__name__)

# Configuration
NODE_ID = None  # Will be set when starting
NODES = {
    1: "http://localhost:5001",
    2: "http://localhost:5002",
    3: "http://localhost:5003"
}

# Local state
local_value = 0
local_timestamp = 0  # Unix timestamp
lock = threading.Lock()

@app.route('/value', methods=['GET'])
def get_value():
    with lock:
        return jsonify({
            'node_id': NODE_ID,
            'value': local_value,
            'timestamp': local_timestamp
        })

@app.route('/value', methods=['POST'])
def update_value():
    global local_value, local_timestamp
    
    data = request.get_json()
    if not data or 'value' not in data:
        return jsonify({'error': 'Missing value'}), 400
    
    new_value = data['value']
    
    with lock:
        local_value = new_value
        local_timestamp = time.time_ns()
        
        # Propagate to other nodes (async)
        propagate_to_other_nodes()
        
        return jsonify({
            'node_id': NODE_ID,
            'value': local_value,
            'timestamp': local_timestamp
        })

@app.route('/sync', methods=['POST'])
def sync():
    global local_value, local_timestamp
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid data'}), 400
    
    received_value = data['value']
    received_timestamp = data['timestamp']
    received_node_id = data['node_id']
    
    with lock:
        # LWW algorithm: keep the value with newer timestamp
        if received_timestamp > local_timestamp:
            print(f"Node {NODE_ID}: Updating from {local_value} to {received_value} (timestamp {received_timestamp} > {local_timestamp})")
            local_value = received_value
            local_timestamp = received_timestamp
        elif received_timestamp == local_timestamp and received_node_id < NODE_ID:
            # Tie-breaker: if same timestamp, lower node ID wins
            print(f"Node {NODE_ID}: Same timestamp, node {received_node_id} < {NODE_ID}, updating")
            local_value = received_value
            # Keep same timestamp
        else:
            print(f"Node {NODE_ID}: Ignoring update (local timestamp {local_timestamp} >= {received_timestamp})")
    
    return jsonify({'status': 'synced'})

def propagate_to_other_nodes():
    current_value = local_value
    current_timestamp = local_timestamp
    
    def propagate():
        for node_id, url in NODES.items():
            if node_id != NODE_ID:
                try:
                    requests.post(
                        f"{url}/sync",
                        json={
                            'value': current_value,
                            'timestamp': current_timestamp,
                            'node_id': NODE_ID
                        },
                        timeout=1
                    )
                    print(f"Node {NODE_ID}: Propagated to node {node_id}")
                except:
                    print(f"Node {NODE_ID}: Failed to reach node {node_id}")
    
    # Run in background thread
    thread = threading.Thread(target=propagate)
    thread.daemon = True
    thread.start()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'alive', 'node_id': NODE_ID})

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python lww_service.py <node_id> <port>")
        print("Example: python lww_service.py 1 5001")
        sys.exit(1)
    
    node_id = int(sys.argv[1])
    port = int(sys.argv[2])
    
    if node_id not in NODES:
        print(f"Node ID must be one of {list(NODES.keys())}")
        sys.exit(1)
    
    NODE_ID = node_id
    app.run(host='0.0.0.0', port=port, debug=False)