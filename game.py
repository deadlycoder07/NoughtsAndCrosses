from network import Network

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
            resp = self.set_new()
            if resp == "W" or resp == "L":
                break
            else:
                self.stat[resp] = self.net.id
        if resp == "W":
            print("Congo You Win")
        else:
            print("Sorry You Lose")
        print("Closing Connection")