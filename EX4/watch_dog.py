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
    
    while True:
        print("in while")
        pingSocket , addr = sock.accept()
        sock.setblocking(10)
        start_time = time.time()
        try:
            replay = pingSocket.recv(2048).decode()
            if (replay == "got responed"):        
                # sock.send("ok".encode())
                print("continue while")
                # break; # exit beacause we recive a signal from ping         
            if(len(replay)> 0 ):
                if (time.time() - start_time)>10:
                    print(f"server {addr[0]} cannot be reached:")
                    # sock.send("TIMEOUT".encode())
                    # sock.close()
                    # sys.exit(0)
            else:
                print(f"another response")
                # sock.send("TIMEOUT".encode())
                # sock.close()
                # sys.exit(0)
        except socket.error as e:
                # sock.send("TIMEOUT".encode())
                print(f"server {addr[0]} cannot be reached:")
                # sock.close()
                # sys.exit(0)
        time.sleep(1)       

watch_dog2()
