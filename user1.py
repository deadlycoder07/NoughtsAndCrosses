from network import Network
import socket 

gamesocket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
class Game():
    def __init__(self):
        self.net = Network()
        self.symbols = {0:'O', 1:'X'}
        self.stat = {1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None, 9:None}
        self.runner = self.loop()
    
    def set_new(self):
        new = int(input("Enter next move"))
        while True:
            if self.stat[new] is None:
                response = self.net.send(self, new)
                break
        return response
    
    def draw(self):
        c = 0
        for i in range(0, 3):
            for j in range(0, 3):
                c += 1
                if self.stat[c] is not None:
                    print(" "+self.symbols[self.stat[c]], end=" ")
                else:
                    print("  ", end=" ")
            print("_________", end="")
    
    def loop(self):
        while True:
            self.draw()
            data, client_address = gamesocket.recvfrom(1024)
            data=data.decode('utf-8')
            self.stat[data]=1
            self.draw()
            new = int(input("Enter next move"))
            self.stat[new]=0
            gamesocket.sendto("".format(new).encode('utf-8'),(socket.gethostname(),8001))
            
            
        if resp == "W":
            print("Congo You Win")
        else:
            print("Sorry You Lose")
        print("Closing Connection")



if __name__ == '__main__':
    gamesocket.bind((socket.gethostname(),8000))
    print("game running on :",socket.gethostname())
    game= Game()
    game.loop()
