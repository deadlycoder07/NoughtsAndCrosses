import pygame
from grid import Grid
import threading
import socket

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '200,100'

surface = pygame.display.set_mode((600,600))
pygame.display.set_caption('Tic-tac-toe')

# create a separate thread to send and receive data from the client
def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

# creating a TCP socket for the server
HOST = '127.0.0.1'
PORT = 3000 
connection_established = False
conn, addr = None, None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT)) #binding connection 
sock.listen(1)   # accepts 1 connection 
 
def receive_data():
    global turn
    while True:
        data = conn.recv(1024).decode() # receive data from the client, it is a blocking method
        data = data.split('-') # the format of the data after splitting is: ['x', 'y', 'yourturn', 'playing']
        x, y = int(data[0]), int(data[1])
        if data[2] == 'yourturn': #alter turns 
            turn = True
        if data[3] == 'False':
            grid.game_over = True
        if grid.get_cell_value(x, y) == 0:
            grid.set_cell_value(x, y, 'O') #reset 
            grid.check_grid(x, y, 'O')

def waiting_for_connection():
    global connection_established, conn, addr
    conn, addr = sock.accept() # wait for a connection, it is a blocking method
    print('client is connected')
    connection_established = True
    receive_data()

# run the blocking functions in a separate thread
create_thread(waiting_for_connection)

grid = Grid()
running = True
player = "X"
turn = True
playing = 'True'

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and connection_established: # move done and conn established successfully 
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.game_over:
                    pos = pygame.mouse.get_pos()
                    cellX, cellY = pos[0] // 200, pos[1] // 200
                    grid.get_mouse(cellX, cellY, player) 
                    if grid.game_over:
                        playing = 'False'
                    send_data = '{}-{}-{}-{}'.format(cellX, cellY, 'yourturn', playing).encode() #sending data 
                    conn.send(send_data)
                    turn = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:
                grid.clear_grid()
                grid.game_over = False
                playing = 'True'
            elif event.key == pygame.K_ESCAPE: # starts a new game logic 
                running = False


    surface.fill((0,0,0)) #black color 

    grid.draw(surface)

    pygame.display.flip()

