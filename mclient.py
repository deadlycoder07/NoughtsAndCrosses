import socket 


def Main(): 
	
	host = '127.0.0.1'
	port = 12345

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
	s.connect((host,port)) 

	 
	message = "The WORLD is Vulnerable and we are going to patch it, NO matter whatever it TAKES!!"
	while True: 
		
		s.send(message.encode('ascii')) 
        	data = s.recv(1024) 
        	print('Received from the server :',str(data.decode('ascii'))) 
		# ask the client whether he wants to continue 
        	ans = input('\nDo you want to continue(y/n) :') 
        	if ans == 'y': 
			continue
	        else: 
			break
	
	s.close() 

if __name__ == '__main__': 
	Main() 
