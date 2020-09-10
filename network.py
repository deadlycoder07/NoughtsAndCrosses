import socket

class Network:

    def __init__(self):
        #AF_INET=IPV4, SOCK_STREAM=TCP Socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.host = "localhost" #Change on client side
        self.port = 1111
        self.id = self.connect()
    
    def connect(self):
        self.server.connect((self.host, self.port))
        print("Connection to {} established".format(self.host))
        #supposed it gets an id from server upon making connection
        return self.server.recv(2048).decode(encoding='UTF-8',errors='strict')

    def send(self, data):
        try:
            self.server.send(data.encode(encoding='UTF-8',errors='strict'))
            reply = self.server.recv(2048).decode(encoding='UTF-8',errors='strict')
            return reply
        except socket.error as e:
            return str(e)