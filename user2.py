import socket 
import tkinter

gamesocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
b = []
label = None

class Game():
    def __init__(self):
        self.symbols = {0:'O', 1:'X'}
        self.stat = {1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None, 9:None}
        self.color = {0:"deep sky blue", 1:"lawn green"}
        self.move_count = 0
        self.labels = ["You move", "Awaiting move from network"]
    
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
            

    def button(self, frame):          
        b=tkinter.Button(frame,padx=1,bg="papaya whip",width=3,text="   ",font=('arial',60,'bold'),relief="sunken",bd=10)
        return b

    def click(self, box):
        b[box].config(text="O", state=tkinter.DISABLED, disabledforeground=self.color[0])
        self.stat[box+1] = 0
        self.move_count += 1
        gamesocket.sendto(str(box).encode('utf-8'),(socket.gethostname(),8000))
        self.check_win()
        label.config(text=self.labels[1],  font=('arial', 20, 'bold'))
        self.update()
        

    def update(self):
        data, client_address = gamesocket.recvfrom(1024)
        self.stat[int(data)+1] = 1
        self.move_count += 1
        b[int(data)].config(text='X', state=tkinter.DISABLED, disabledforeground=self.color[1])
        label.config(text=self.labels[0],  font=('arial', 20, 'bold'))
        self.check_win()
        return

    def gui(self):
        tk = tkinter.Tk()
        tk.title("Tic Tac Toe")
        c = 0
        for i in range(3):
            for j in range(3):
                b.append(self.button(tk))
                b[c].config(command = lambda box=c:self.click(box))
                b[c].grid(row=i, column=j)
                c += 1
        label = tkinter.Label(text=self.labels[0], font=('arial', 20, 'bold'))
        label.grid(row=3, column=0, columnspan=3)
        tk.mainloop()

    def check_win(self):
        x = None
        if self.move_count == 9:
            print("Itsa draw")
            exit(0)
        else:
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
            if x == 1:
                print("Sorry you lose")
                exit(0)
            elif x == 0:
                print("Congrats you win")
                exit(0)


if __name__ == '__main__':
    gamesocket.bind((socket.gethostname(),8001))
    print("game running on :",socket.gethostname())
    game= Game()
    game.gui()
