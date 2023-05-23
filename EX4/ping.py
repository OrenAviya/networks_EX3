import os
import socket
import struct
import time

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0 

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

def ping(host):
    count_iter = 1

    # Create a raw socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    if isinstance(sock, socket.socket):
        print("socket created successfully\n")
    else:
        print("socket creation failed. \n")
    
    sock.settimeout(5)

    while True:
        # Create the ICMP echo request packet
        pid = os.getpid() & 0xFFFF
        ch_sum = 0 
        head = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, ch_sum, pid, count_iter)
        start_time = time.time()
        data = struct.pack("d",start_time )
        # Calculate the checksum for the packet
        my_checksum = checksum(head + data)
        # create the icmp packet for sending
        head = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), pid, count_iter)
        icmp_packet = head + data

        #  Send the packet
        destIP = (host, count_iter)
        try:
            sock.sendto(icmp_packet, destIP )
        except socket.error as e:
            print(f"Socket error send failed: {e}")
        
        try:
            while True:
                # Receive the response packet
                try:
                    data, addr = sock.recvfrom(1024)
                except socket.error as e:
                    print(f"Socket error recived failed: {e}")
                
                end_time = time.time()
                elapsed_time = end_time - start_time

                # Extract the ICMP type and code from the response packet
                icmp_type, icmp_code = struct.unpack('!BB', data[20:22])

                if icmp_type == ICMP_ECHO_REPLY and icmp_code == 0:
                    # Extract (for printing) the number of bytes (len), IP, sequence number, and time from the response packet
                    ip = addr[0]
                    seq_num_reply = struct.unpack('!H', data[6:8])[0]
                    len_data = len(data)
                    time_data = struct.unpack('!f', data[28:32])  # Assuming the time field is a float (4 bytes)
                    elapsed_time = time_data[0]
                    print(f"{len_data} bytes from {ip}: icmp_seq={seq_num_reply} time={elapsed_time}s")
                    break
        except socket.timeout:
            print("Request timed out")

        count_iter += 1

host = '8.8.8.8'
ping(host)
