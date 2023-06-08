from scapy.all import *
from scapy.contrib.igmp import IGMP
from scapy.layers.inet import IP, TCP, UDP, ICMP



def process_packet(packet):
        if packet.haslayer(IP):
            ip_packet = packet[IP]
            protocol = ip_packet.proto

        if protocol == 6:
            print("TCP packet")
            packet_kind = TCP
        elif protocol == 17:
            print("UDP packet")
            packet_kind = UDP
        elif protocol == 1:
            print("ICMP packet")
            packet_kind = ICMP
        elif protocol == 2:
            print("IGMP packet")
            packet_kind = IGMP
        else:
            packet_kind = IP
            print("Raw packet")

        # Extract relevant fields from the packet
        source_ip = ip_packet.src
        dest_ip = ip_packet.dst
        # Other packet information
        timestamp = packet.time
        total_length = len(packet)
        transport_layer = packet[packet_kind]
        source_port = None
        dest_port = None
        cache_flag = None
        steps_flag = None
        type_flag = None
        status_code = None
        cache_control = None

        if packet.haslayer(packet_kind):
            if ICMP in packet:
                proto = "ICMP"
                source_ip = packet[IP].src
                dest_ip = packet[IP].dst
                total_length = packet[IP].len

            elif TCP or UDP in packet:

                source_port = transport_layer.sport
                dest_port = transport_layer.dport

                cache_flag = transport_layer.flags.C
                steps_flag = transport_layer.flags.S
                type_flag = transport_layer.flags.A
                status_code = transport_layer.flags.F
                cache_control = transport_layer.flags.P


            data = transport_layer.payload
            # Generate the hexadecimal representation of the payload
            data_hex = hexdump(data, dump=True)

        print(f"{packet_kind} Request from src {source_ip}")
        # Write the packet details to the file
        with open("322273301_325195774.txt", "a") as file:

            file.write(f'source_ip: {source_ip} , dest_ip: {dest_ip} ,source_port: {source_port}, dest_port: {dest_port}, timestamp: {timestamp}, total_length: {total_length}, cache_flag: {cache_flag}, steps_flag: {steps_flag}, type_flag: {type_flag}, status_code: {status_code}, cache_control: {cache_control}, data: {data}\n' )




# Start the packet sniffer
sniff(filter="icmp", prn=process_packet) # סעיף 2
#sniff(prn=process_packet, filter="ip", store=0, iface= 'br-a14b571ac5c4')
