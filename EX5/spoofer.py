from scapy.all import *
from scapy.layers.inet import IP, TCP, ICMP, UDP


def cal_checksum(data):
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


def spoof_ip(packet):  # packet type is ICMP / TCP / UDP
    # create a raw socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    # Create a UDP socket
    #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    scapy_packet = IP(packet)

    # Send the modified packet
    sock.sendto((packet), ('localhost', 0))
    #sock.sendto(packet, (packet[], 0))
    sock.close()


def create_TCP_spoof_packet():
    source_ip = '1.2.3.4'
    dest_ip = "127.0.0.1"
    source_port =5000
    dest_port =12345
    data = b'fake TCP'
    ip_header = struct.pack('!BBHHHBBH4s4s', 69, 0, 28 + len(data), 0, 21, socket.IPPROTO_TCP,
                     0, socket.htons(0), socket.inet_aton(source_ip), socket.inet_aton(dest_ip))

    tcp_header = struct.pack('!HHLLBBHHH',
                             source_port,
                             dest_port,
                             0,  # Sequence number
                             0,  # Acknowledgment number
                             69,  # Data offset and reserved bits
                             0,  # TCP flags (set later)
                             8192,  # Window size
                             0,  # Checksum (set later)
                             0)  # Urgent pointer

    pseudo_header = struct.pack('!4s4sBBH',
                                socket.inet_aton(source_ip),
                                socket.inet_aton(dest_ip),
                                0,  # Placeholder for zero byte
                                socket.IPPROTO_TCP,
                                len(tcp_header) + len(data))

    # Calculate the TCP checksum
    checksum = cal_checksum(pseudo_header + tcp_header + data)
    tcp_header = struct.pack('!HHLLBBH',
                             source_port,
                             dest_port,
                             0,  # Sequence number
                             0,  # Acknowledgment number
                             69,
                             0,
                             8192)
    tcp_header += struct.pack('H', checksum) + struct.pack('!H', 0)

    tcp_packet = ip_header + tcp_header + data
    return tcp_packet


def create_UDP_spoof_packet():
    data= b'fake UDP'
    source_ip = '1.2.3.4'
    dest_ip = "127.0.0.1"
    source_port = 5000
    dest_port= 12345
    udp_header = struct.pack('!HHHH',
                             source_port,
                             dest_port,
                             8 + len(data),  # Length of UDP header + data
                             0)  # Placeholder for checksum calculation
    ip_header = struct.pack('!BBHHHBBH4s4s', 69, 0, 28 + len(data), 0, 21, socket.IPPROTO_UDP,
                0, socket.htons(0), socket.inet_aton(source_ip), socket.inet_aton(dest_ip))


    udp_packet = ip_header+ udp_header + data
    return udp_packet


def create_icmp_spoof_packet():
    # Create the IP header
    ip_header = struct.pack('!BBHHHBBH4s4s', 69, 0, 28, 0, 21, socket.IPPROTO_ICMP, 0, socket.htons(0),
                            socket.inet_aton("1.2.3.4"), socket.inet_aton("127.0.0.1"))

    # Create the ICMP header and data
    icmp_type = 8  # ICMP Echo Request type
    icmp_code = 0  # ICMP Echo Request code
    icmp_checksum = 0  # Placeholder for checksum calculation
    icmp_identifier = 1234  # Identifier field
    icmp_sequence = 1  # Sequence number field
    icmp_data = b'fake ICMP!'  # Data payload

    icmp_header = struct.pack('!BBHHH',
                              icmp_type,
                              icmp_code,
                              icmp_checksum,
                              icmp_identifier,
                              icmp_sequence)

    # Calculate the ICMP checksum
    checksum = cal_checksum(icmp_header + icmp_data)
    icmp_header = struct.pack('!BBHHH',
                              icmp_type,
                              icmp_code,
                              checksum,
                              icmp_identifier,
                              icmp_sequence)

    # Create the complete ICMP packet
    icmp_packet = ip_header + icmp_header + icmp_data

    return icmp_packet  # packet


tcp_packet = create_TCP_spoof_packet()
udp_packet = create_UDP_spoof_packet()
icmp_packet = create_icmp_spoof_packet()

#spoof_ip(udp_packet)
#print("spoof udp")
#spoof_ip(tcp_packet)
#print("spoof tcp")
spoof_ip(icmp_packet)
print("spoof icmp")