import socket
import time
import threading
import sys

def watch_dog():
    # for debugging
    # print("in watchdog")

    # create a socket and defined it to "localhost" and port 3000 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try: #check if created sucsses
        sock.bind(('localhost', 3000))
        print("Socket binding successful")
    except socket.error as e:
        print(f"Socket binding failed: {e}")
    
    sock.listen(1) # listen for the connect-ask from the ping thread we open
    # we set the "timeout" to 10, so if there no response for more than 10 seconds it will throw an error 
    # , and print "server cannot be reached"
    sock.settimeout(10)

    while True:
        # start the watch dog timer , to count time  
        start_time = time.time()
        # if the connection won't happen in 10 sec it will throw an error automaticly
        try:
            pingSocket , addr = sock.accept()
            print (f"pingsocket:{pingSocket}")
        except socket.error as e:
            print(f"server cannot be reached ({e})")
            sys.exit(0)
        # if the connection was happned,we will check the time that takes to the ping to send 
        # the ping and get the response when the ping get the response it will sent the "got response" massege
        # to watch dog , how check if it takes more than 10 sec , if so - it will throw an error.
        # if every thing is OK it will continue the wile loop and restart the timer.
        try:
            replay = pingSocket.recv(1024).decode()
            if (replay == "got responed"):        
                print("continue while")
                continue; #  beacause we recive a signal from ping         
            elif(len(replay)> 0 ):
                if (time.time() - start_time)>10:
                    print(f"server {addr[0]} cannot be reached:")
                    raise socket.error           
        except socket.error as e:
                print(f"server {addr[0]} cannot be reached:")
                raise socket.error       
        if (time.time() - start_time)>10:
            print("server cannot be reached.")
            raise socket.error
        time.sleep(1)       

if __name__ == '__main__':
    watch_dog()
