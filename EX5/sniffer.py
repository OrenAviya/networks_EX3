import sys

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
        elif ICMP in ip_packet:
            print("ICMP packet")
            packet_kind = ICMP
        elif protocol == 2:
            print("IGMP packet")
            packet_kind = IGMP
        else:
            print(f"protocool: {protocol}")
            print("Raw packet")

        # Extract relevant fields from the packet
        source_ip = ip_packet.src
        dest_ip = ip_packet.dst

        if packet.haslayer(packet_kind):
            transport_layer = packet[packet_kind]

            # Other packet information
            timestamp = packet.time
            total_length = len(packet)
            if TCP in packet:
                source_port = transport_layer.sport
                dest_port = transport_layer.dport
                cache_flag = transport_layer.flags.C
                steps_flag = transport_layer.flags.S
                type_flag = transport_layer.flags.A
                status_code = transport_layer.flags.F
                cache_control = transport_layer.flags.P
            else:
                source_port = None
                dest_port = None
                cache_flag = None
                steps_flag = None
                type_flag = None
                status_code = None
                cache_control = None
            data = transport_layer.payload
            # Generate the hexadecimal representation of the payload
            data_hex = hexdump(data, dump=True)


        # Write the packet details to the file
        with open("322273301_325195774.txt", "a") as file:

            file.write("{ source_ip: " + source_ip + ", dest_ip: " + dest_ip +
                       ", source_port: " + str(source_port) + ", dest_port: " +
                       str(dest_port) + ", timestamp: " + str(timestamp) +
                       ", total_length: " + str(total_length) + ", cache_flag: " +
                       str(cache_flag) + ", steps_flag: " + str(steps_flag) +
                       ", type_flag: " + str(type_flag) + ", status_code: " +
                       str(status_code) + ", cache_control: " + str(cache_control) +
                       ", data: " + data_hex + " }\n")

        print(f"{packet_kind} Request from src {source_ip}")


# Start the packet sniffer
sniff(filter="ip", prn=process_packet, store=0, iface = "lo") # סעיף 2
#sniff(prn=process_packet, filter="ip", store=0, iface= 'br-a14b571ac5c4') //
