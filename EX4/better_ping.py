import os
import socket
import struct
import threading
import time
import sys

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0 

"""
this function is similar to ping but the ping is conclude the "while" loop and the timer,
so it send & recive with no stop untill timeout error occur or keyboard intterupted.
In better_ping we write the "one_send_recv_ping" which doing just one send and recive it's replay
,in the main we insert the while loop, and the watch dog has the responsibility on the timeout error.

"""
def one_send_recv_ping(host):
    
    # Create a raw socket  , in raw socket no need to "connect" to the server 
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    if isinstance(sock, socket.socket):
        print("socket ping created successfully\n")
    else:
        print("socket creation failed. \n")
    
    # -------------------------------------------------
     # """sending a ping + get a response: ONE TIME:"""
    #  ------------------------------------------------

    # Create the ICMP echo request packet
    pid = os.getpid() & 0xFFFF
    ch_sum = 0 
    head = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, ch_sum, pid, 1)
    data = struct.pack("d",time.time())
    
    # Calculate the checksum for the packet
    my_checksum = checksum(head + data)
    
    # create the icmp packet for sending, with the checksum calculation
    head = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), pid, 1)
    icmp_packet = head + data
    
    #Defined the destination to send , to the host we got as a param:
    destIP = (host, 1)
    #  Try to send the packet:
    try:
        sock.sendto(icmp_packet, destIP )
        print(f"Socket send file")    
    except socket.error as e:
        print(f"Socket error send failed: {e}")
    # If the packet wes sended , a replay shuld occured:
    
    while True:
        # Receive the response packet
        try:
            #  Because there is no timer here , the code waiting until 
            # a replay will recived.
            # To handle with that the watch dog is waiting to the message from the ping. 
            # this message will sent after the ping get the replay & printing output
            # if all this process will take more than 10 sec ,
            # the watch dog will throw an error and stop the program 
            print(f"Socket wait for data")
            data, addr = sock.recvfrom(1024)
            print(f"data: {data} ,addres {addr}")
        except socket.error as e:
            print(f"Socket error recived failed: {e}")
            # If no replay was recieved  
            return 0
        

        # Extract the ICMP type and code from the response packet
        icmp_type, icmp_code = struct.unpack('!BB', data[20:22])
        print(f"icmptype = {icmp_type} , icmpcode = {icmp_code}")
        #If it is the correct replay from the "8.8.8.8" host
        if icmp_type == ICMP_ECHO_REPLY and icmp_code == 0:
            
            # Extract the number of bytes (len),
            #  IP, sequence number, 
            # and time from the response packet
            ip = addr[0]
            seq_num_reply = struct.unpack('!H', data[6:8])[0]
            len_data = len(data)
            time_data = struct.unpack('!f', data[28:32])  # Assuming the time field is a float (4 bytes)
            elapsed_time= time_data[0] 
            # printing the details
            print(f"{len_data} bytes from {ip}: icmp_seq={seq_num_reply} time={elapsed_time}s")
            return 1
            break
        else :
            print("error")


def checksum(data):
    # Calculate the checksum of the data
    checksum = 0
    countTo = (len(data) // 2) * 2

    for count in range(0, countTo, 2):
        word = (data[count + 1] << 8) + data[count]
        checksum += word

    if countTo < len(data):
        checksum += data[len(data) - 1]

    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum += (checksum >> 16)
    checksum = ~checksum & 0xFFFF

    return checksum

if __name__ == '__main__':
    
    host = '8.8.8.8'
    # start the watchdog server on different thread.
    t_watchdog = threading.Thread(target=lambda: os.system(f'python3 watch_dog.py'))
    t_watchdog.start()
    
    time.sleep(1)
    try:
        # we send&recive untill keyboard interupted or timeout error:
        while True:
            # one_send_recv_ping - return 1 if the send sucsess and got replay 
            is_sent = one_send_recv_ping(host)
            
            # After the ping sucsess
            # Create the socket to connect and identify watchdog
            sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if isinstance(sock2, socket.socket):
                print("socket created successfully\n")
            else:
                print("socket creation failed. \n")
            # Connect to watchdog       
            if(sock2.connect_ex(('localhost', 3000))==0):
                print("socket connected successfully\n")
            else:
                print(f"Socket connect failed")
            
            if (is_sent == 1):
                # Identify the watch dog that response was recived
                message = "got responed"
                sock2.send(message.encode())

    except socket.error as e:
        sock2.close()


