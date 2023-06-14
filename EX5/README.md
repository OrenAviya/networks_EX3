
##Task A – 15%
Write your own sniffer for capturing packets.  Your sniffer should be able to sniff the following protocols:
-	TCP
-	UDP 
-	ICMP
-	IGMP
-	RAW (other - default)
Run your Ex 2 from Networks Course. Use your sniffer to sniff the TCP packets and write them out into a txt file named after your IDs. The format of each packet should be { source_ip: <input>, dest_ip: <input>, source_port: <input>, dest_port: <input>, timestamp: <input>, total_length: <input>, cache_flag: <input>, steps_flag: <input>, type_flag: <input>, status_code: <input>, cache_control: <input>, data: <input> }
The data output may be unreadable in ASCII form so write the output as hexadecimal.
In the paragraph following your Explanations of this task, please answer the following question:
Question
-	Why do you need the root privilege to run a sniffer program? Where does the program fail if it is executed without the root privilege? 
Submission – sniffer.py and relative pcap file
Write detailed research in your PDF about Your sniffer abilities and limitations
##Task B – 15%
Write a spoofer for spoofing packets. Your spoofer should be able to spoof packets  by using the following protocols:
-	ICMP
-	UDP
-	TCP (Bonus 3 points to the assignment)

The spoofer should fake the sender’s IP and has a valid response. Your code should be able to spoof other protocols with small changes.
In the paragraph following your Explanations of this task, please answer the questions:
 Question 1.
Can you set the IP packet length field to an arbitrary value, regardless of how big the actual packet is?
Question 2.
Using the raw socket programming, do you have to calculate the checksum for the IP header?
Write detailed research in your PDF about Your spoofer abilities and limitations

##Task C – 10%
The objective of this task is to use Scapy to estimate the distance, in terms of number of routers, between your VM and a selected destination. This is basically what is implemented by the traceroute tool. In this task, we will write our own tool. The idea is quite straightforward: just send an packet (any type) to the destination, with its Time-To-Live (TTL) field set to 1 first. This packet will be dropped by the first router, which will send us an ICMP error message, telling us that the time-to-live has exceeded. That is how we get the IP address of the first router. We then increase our TTL field to 2, send out another packet, and get the IP address of the second router. We will repeat this procedure until our packet finally reach the destination. It should be noted that this experiment only gets an estimated result, because in theory, not all these packets take the same route (but in practice, they may within a short period of time).

* You should write your tool to perform the entire procedure automatically.

##Task D – 50%
@Before -read Appendix B for composing the LAN of docker containers.
In this task, you will combine the sniffing and spoofing techniques to implement the following sniff-and-then-spoof program. You need two machines on the same LAN. From machine A, you ping an IP X. This will generate an ICMP echo request packet. If X is alive, the ping program will receive an echo reply, and print out the response. Your sniff-and-then-spoof program runs on the attacker machine, which monitors the LAN through packet sniffing. Whenever it sees an ICMP echo request, regardless of what the target IP address is, your program should immediately send out an echo reply using the packet spoofing technique. 
Please follow those steps:
1.	Compose the Docker Containers that are in the Zip from the Moodle (The TAs showed you how to do so in Tirgul 09)
•	Note: If it doesn’t work properly you can create a LAN by composing few Machines on your VirtualBox 
2.	Run your Ex_4 codes from Networks Course in this new LAN. Use your sniffer from Task A to sniff the ICMP packets from the seed-attacker. Peel off the needed data for spoofing the packets, and return a packet which made by you. 
a.	First run – send a ping from Host A to Host B
b.	Second run – send a ping from Host A to a WAN IP (e.g., google DNS – 8.8.8.8)
c.	Third run – send a ping from Host A to a fake IP.
d.	Fourth run – send a ping from Host A to fake IP in your LAN
3.	Write detailed research in your PDF about Task C
##Task E - 10%
Please show how you can use your sniffer program to capture the password when somebody is using telnet on the network that you are monitoring. You may need to modify your sniffer code to print out the data part of a captured TCP packet (telnet uses TCP). It is acceptable if you print out the entire data part, and then manually mark where the password (or part of it) is.

Submission – sniffing_passwords.py and relative pcap file
Write detailed research in your PDF about Your sniffing_password.py output
 

