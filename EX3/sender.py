import os.path
import subprocess
import socket

# Authentication Check:
id1 = 5774
id2 = 3301


def AuthenticationCheck(sock):
    id_xor = (str)(id1 ^ id2).encode()
    # receive the response
    response = sock.recv(4096)
    # print("response : " ,*response )
    # print("suppose to be:" ,*id_xor)
    if response == id_xor:
        # authentication successful
        result = 1
        print("authentication success\n")
    else:
        # authentication failed
        result = 0
        print("authentication failed\n")

    return result



# Define the host and port of the receiver
host = 'localhost'
port = 8000

fileName = "file"
filesize = os.path.getsize(fileName)
# Open the file , read the first and second Half of the file, to be sent
with open(fileName, 'rb') as f:
    n = (filesize // 2)
    file_data1 = f.read(n)
    # Move the file pointer to the half of the file
    f.seek(-n, os.SEEK_END)
    file_data2 = f.read(n)


while True:
    # Create a socket object and connect to the receiver
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # checking if the creation success
    if isinstance(sock, socket.socket):
        print("socket created successfully\n")
    else:
        print("socket creation failed. \n")

    # set the congestion control algorithm to reno
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, 'reno'.encode())

    # check if the connection success connect_ex & connect-is the same but the return value, A return value of 0 indicates
    # that the connection was successful, while a non-zero value indicates that the connection failed.
    if sock.connect_ex((host, port)) == 0:
        print("Connection successful!\n")
    else:
        print("Connection failed.\n")

    # Send the file data to the receiver
    sock.send(file_data1)

    # Authentication Check:
    if AuthenticationCheck(sock) == 1:
        print("the first half was sended size: ", len(file_data1))
        # change CC algorithm to cubic:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, 'cubic'.encode())
        # sending part 2
        sock.send(file_data2)
       
        print("the second half was sended, size: " , len(file_data2))
    else:
        sock.close()
        print("authentication failed , stop sending")
        break

    # User decision:
    print("You can help us with data gathering , do you want to sending the file again? ")
    ans = input("[Y] to yes and any other letter to exit\n")
    if ans == 'Y' or ans == 'y':
        print("sending again\n")
        sock.send("keep going".encode())
        sock.close()
    else:
        print("exit\n")
        # send bye to the reciver
        sock.send("bye".encode())
        # Close the socket
        sock.close()
        break
