import tkinter
import socket 

gamesocket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
b = []


class Game():
    def __init__(self):
        self.symbols = {0:'O', 1:'X'}
        self.stat = {1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None, 9:None}
        self.color = {0:"deep sky blue", 1:"lawn green"}
        self.move_count = 0
        self.labels = ["You move", "Awaiting move from network"]

        tk = tkinter.Tk()
        tk.title("Tic Tac Toe")
        c = 0
        
        for i in range(3):
            for j in range(3):
                b.append(self.button(tk))
                b[c].config(command = lambda box=c:self.click(box))
                b[c].grid(row=i, column=j)
                c += 1
        
        self.label = tkinter.Label(text=self.labels[1], font=('arial', 20, 'bold'))
        self.label.grid(row=3, column=0, columnspan=3)
        tk.mainloop()
        self.update()

    def button(self, frame):          
        b=tkinter.Button(frame,padx=1,bg="papaya whip",width=3,text="   ",font=('arial',60,'bold'),relief="sunken",bd=10)
        return b

    def click(self, box):
        b[box].config(text="X", state=tkinter.DISABLED, disabledforeground=self.color[0])
        self.stat[box+1] = 1
        self.move_count += 1
        gamesocket.sendto(str(box).encode('utf-8'),(socket.gethostname(),8001))
        self.check_win()
        print(self.stat)
        self.label.config(text=self.labels[1],  font=('arial', 20, 'bold'))
        self.update()

    def update(self):
        data, client_address = gamesocket.recvfrom(1024)
        self.stat[int(data)+1] = 0
        print(int(data))
        self.move_count += 1
        b[int(data)].config(text='O', state=tkinter.DISABLED, disabledforeground=self.color[1])
        self.label.config(text=self.labels[0],  font=('arial', 20, 'bold'))
        self.check_win()
        return

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
            if self.stat[3] == self.stat[6] and self.stat[3] == self.stat[9]:
                x =  self.stat[3]
            if self.stat[1] == self.stat[5] and self.stat[1] == self.stat[9]:
                x =  self.stat[1]
            if self.stat[3] == self.stat[5] and self.stat[3] == self.stat[7]:
                x =  self.stat[3]
            if x == 0:
                print("Sorry you lose")
                exit(0)
            elif x == 1:
                print("Congrats you win")
                exit(0)


if __name__ == '__main__':
    gamesocket.bind((socket.gethostname(),8000))
    print("game running on :",socket.gethostname())
    game = Game()
