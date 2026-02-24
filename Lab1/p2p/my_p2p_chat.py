import socket
import threading
import sys

# example:
# terminal A:
# python3 Lab1/p2p/my_p2p_chat.py 5001 127.0.0.1:5000
# terminal B: 
# python3 Lab1/p2p/my_p2p_chat.py 5000 127.0.0.1:5001

def listener(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))
    
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"\n{data.decode()}")
        print("> ", end="", flush=True)
        

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python chat.py <listen_port> <peer_ip:peer_port>")
        sys.exit(1)
    
    listen_port = int(sys.argv[1])
    peer_ip, peer_port = sys.argv[2].split(':')
    peer_port = int(peer_port)
    
    threading.Thread(target=listener, args=(listen_port,), daemon=True).start()
    
    name = str(input("login: "))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while True:
        msg = input("> ")
        sock.sendto(f"{name}: {msg}".encode(), (peer_ip, peer_port))