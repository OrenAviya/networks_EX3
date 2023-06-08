from scapy.all import *

def traceroute(dest):
    ttl = 1
    max_hops = 30
    dst_ip = socket.gethostbyname(destination)

    while ttl <= max_hops:
        # Create an ICMP packet with increasing TTL
        packet = IP(dst=dst_ip, ttl=ttl) / ICMP()

        # Send the packet and receive the response
        reply = sr1(packet, verbose=False, timeout=2)

        if reply is None:
            # No response received within the timeout
            print(f"{ttl}. * * *")
        elif reply.type == 11:
            # ICMP Time Exceeded message received
            print(f"{ttl}. {reply.src}")
        elif reply.type == 0:
            # ICMP Echo Reply received (destination reached)
            print(f"{ttl}. {reply.src} (Destination Reached)")
            break

        ttl += 1


# Example usage
destination = "www.google.com"  # Replace with the desired destination
traceroute(destination)
