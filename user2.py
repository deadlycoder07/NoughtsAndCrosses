from network import Network
import socket 

gamesocket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class Game():
    def __init__(self):
        self.symbols = {0:'O', 1:'X'}
        self.stat = {1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None, 9:None}
        self.runner = self.loop()
    
    def draw(self):
        c = 0
        for i in range(0, 3):
            for j in range(0, 3):
                c += 1
                if self.stat[c] is not None:
                    print("| "+self.symbols[self.stat[c]], end=" |")
                else:
                    print("|  ", end=" |")
            print("\n--------------------")
    
    def loop(self):
        while True:
            x = self.check_win()
            if x is 1:
                print("The winner is Not You")
                print("Closing Connection")
                exit(0)
            elif x is 0:
                print("The winner is You")
                print("Closing Connection")
                exit(0)
            new = int(input("Enter next move\n"))
            while True:
                if self.stat[new] is None:
                    self.stat[new]=0
                    gamesocket.sendto(str(new).encode('utf-8'),(socket.gethostname(),8000))
                    break
                else:
                    new = int(input("Enter a valid move\n"))
            self.draw()
            x = self.check_win()
            if x is 1:
                print("The winner is Not You")
                print("Closing Connection")
                exit(0)
            elif x is 0:
                print("The winner is You")
                print("Closing Connection")
                exit(0)
            data, client_address = gamesocket.recvfrom(1024)
            data = data.decode('utf-8')
            self.stat[int(data)] = 1
            self.draw()
            

    def check_win(self):
        x = None
        if self.stat[1] == self.stat[2] and self.stat[1] == self.stat[3]:
            x = self.stat[1]
        if self.stat[4] == self.stat[5] and self.stat[4] == self.stat[6]:
            x = self.stat[4]
        if self.stat[7] == self.stat[8] and self.stat[7] == self.stat[9]:
            x = self.stat[7]
        if self.stat[1] == self.stat[4] and self.stat[1] == self.stat[7]:
            x =  self.stat[1]
        if self.stat[2] == self.stat[5] and self.stat[2] == self.stat[8]:
            x =  self.stat[2]
        if self.stat[3] == self.stat[5] and self.stat[3] == self.stat[9]:
            x =  self.stat[3]
        if self.stat[1] == self.stat[5] and self.stat[1] == self.stat[9]:
            x =  self.stat[1]
        if self.stat[3] == self.stat[5] and self.stat[3] == self.stat[7]:
            x =  self.stat[3]
        return x


if __name__ == '__main__':
    gamesocket.bind((socket.gethostname(),8001))
    print("game running on :",socket.gethostname())
    game= Game()
    game.loop()
