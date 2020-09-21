import socket 

gamesocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

gamesocket.bind((socket.gethostname(), 8000))
print("Running on :", socket.gethostname())

recv_data = gamesocket.recv(4096).decode('utf-8')
print("Recieved: ",recv_data)

if recv_data == "PING":
    data = "PONG"
    print("Sending: PONG")
    gamesocket.sendto(str(data).encode('utf-8'),(socket.gethostname(),8001))