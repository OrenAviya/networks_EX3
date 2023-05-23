import socket
import time
import threading
import sys


def watch_dog2():
    print("in watchdog")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(('localhost', 2000))
        print("Socket binding successful")
    except socket.error as e:
        print(f"Socket binding failed: {e}")
    sock.listen(5)
    sock.settimeout(10)
    
    while True:
        start_time = time.time()
        try:
            pingSocket , addr = sock.accept()
            print (f"pingsocket:{pingSocket}")
        except socket.error as e:
            print(f"server cannot be reached ({e})")
            sys.exit(0)
        try:
            replay = pingSocket.recv(1024).decode()
            if (replay == "got responed"):        
                print("continue while")
                continue; #  beacause we recive a signal from ping         
            
            elif(len(replay)> 0 ):
                if (time.time() - start_time)>10:
                    return 0
                    print(f"server {addr[0]} cannot be reached:")
                    
        except socket.error as e:
                return 0
                print(f"server {addr[0]} cannot be reached:")
                # sock.close()
                # sys.exit(0)
                sys.exit(0)
        if (time.time() - start_time)>10:
            print("server cannot be reached.")
            return 0
        
        time.sleep(1)       

if __name__ == '__main__':
    watch_dog2()
