from scapy.layers.inet import TCP
from scapy.all import *
i=0
def sniff_telnet_packets(packet):
    global i
    if packet.haslayer(TCP) and packet[TCP].dport == 23:
        i+=1
        payload = packet[TCP].payload
        if payload:
            print(f"Telnet packet captured: {payload}")
            with open("telnet_packets.txt", "a") as file:
                file.write(f"{i}: {payload}\n")

# Sniff Telnet packets
sniff(filter="tcp", prn=sniff_telnet_packets , iface = 'br-a14b571ac5c4')
