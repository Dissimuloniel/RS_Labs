## How to run?
`python3 node_service.py <node_id> <port>` \
where node_id is 1, 2 or 3 and port is 5001, 5002, 5003 accordingly 

#### Like this:
Terminal 1: `python3 node_service.py 1 5001`\
Terminal 2: `python3 node_service.py 2 5002`\
Terminal 3: `python3 node_service.py 3 5003`

## Usage 

Get node state: \
`curl http://localhost:5001/value`

Update value: \
`curl -X POST http://localhost:5001/value -H "Content-Type: application/json" -d '{"value": 42}'`

Sync example: 
``` bash
curl -X POST http://localhost:5001/value -H "Content-Type: application/json" -d '{"value": 100}'

curl http://localhost:5001/value
curl http://localhost:5002/value
curl http://localhost:5003/value
```

LLW example: 
``` bash
curl -X POST http://localhost:5001/value -H "Content-Type: application/json" -d '{"value": 200}'
curl -X POST http://localhost:5002/value -H "Content-Type: application/json" -d '{"value": 300}'

curl http://localhost:5001/value
curl http://localhost:5002/value
curl http://localhost:5003/value
```