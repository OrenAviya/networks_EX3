from scapy.all import *
from scapy.layers.inet import IP, TCP, ICMP, UDP

def fake_replay(packet):

    if packet.haslayer(ICMP) and packet[ICMP].type == 8:

        # make fake ICMP echo reply packet
        dest = str(packet[IP].dst)
        src = str(packet[IP].src)

        # Create fake ICMP echo reply packet
        reply = IP(dst = src, src= '1.2.3.4') / ICMP(type="echo-reply", code=0)

        # Send the fake reply
        send(reply)
        print(f"ICMP echo reply from {'1.2.3.4'} to {src} was sent")



if __name__ == "__main__":
    #sniff packets from protocol ICMP
    #then spoof and send back a fake replay packet
    sniff(filter="icmp", prn=fake_replay , iface ='br-a14b571ac5c4' )