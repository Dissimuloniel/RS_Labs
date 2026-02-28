## How to run?
Terminal 1: `python node_service.py 1 5001`\
Terminal 2: `python node_service.py 2 5002`\
Terminal 3: `python node_service.py 3 5003`

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
