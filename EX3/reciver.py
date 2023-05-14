import socket
import time
import os

time_list1 = []
time_list2 = []
id1 = 5774
id2 = 3301

fileName = "file"
filesize = os.path.getsize(fileName)

##Create a TCP connection between the sender and receiver
# Define the host and port to listen on
host = 'localhost'
port = 8000

# Create a socket object and bind it to the host and port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((host, port))
    # Listen for incoming connections
    sock.listen()
    print(f"Listening on {host}:{port}")

    while True:
        # Accept a connection and receive the file data
        conn, addr = sock.accept()
        print(f"Connection established from {addr}")
        # change CC algorithm to reno:
        conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, "reno".encode())
        # measure the time it is take to recive the data
        start_time = time.time()
        all_file = ""
        while True:
            data_part1 = conn.recv(4096).decode()
            all_file += data_part1
            if len(all_file) >= filesize/2  :
                break
        
        end_time = time.time()
        total_time1 = end_time - start_time
        time_list1.append(total_time1)
        if len(all_file) > 0:
            print("the first part was recived in size: ", len(all_file))
       
        id_xor = (str)(id1 ^ id2).encode()
        conn.send(id_xor)
        print("send the auth 1")

        # recive the second part:
        # change CC algorithm to cubic:
        conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, "cubic".encode())
        # measure the time it is take to recive the data
        start_time = time.time()
        while True:
            data_part2 = conn.recv(4096).decode()
            all_file += data_part2
            if len(all_file) >= filesize:
                break
            
        end_time = time.time()
        total_time2 = end_time - start_time
        time_list2.append(total_time2)
        if len(all_file) > 0:
            print("all file was recived in size: ", len(all_file))
       
        # recive the exit/keep going massagefrom the server.
        data = conn.recv(4096).decode()
        if data == "bye":
            print("recive the massage: ", *data)
            # Print the total time it took to receive the file
            print("Time to receive part 1: ")
            for i in range(len(time_list1)):
                print("run ", i, ": ", time_list1[i], "\n")
            print("Time to receive part 2: ")
            for i in range(len(time_list2)):
                print("run ", i, ": ", time_list2[i], "\n")
            avg_time_part_1 = sum(time_list1) / len(time_list1)
            avg_time_part_2 = sum(time_list2) / len(time_list2)
            print("Average time for part 1: ", avg_time_part_1)
            print("Average time for part 2: ", avg_time_part_2)
            # close the connection and the socket.
            conn.close()
            sock.close()
            break
        else:
            print("recive the massage: ", *data)
            # close this connection but keep the socket on for the next connections
            conn.close()
