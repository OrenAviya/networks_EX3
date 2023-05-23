
### Myping - 60%
The ping command is used to check the connection between 2 machines. In this part, you will implement the "ping" command (see picture below).
 
You will write a program called "ping.py" which will get an argument indicating which host to ping.
Usage: python ping.py <ip> (just like the ping command)
The program will send an ICMP ECHO REQUEST to the host, and when receiving ICMP-ECHO-REPLY, the program will send the next ICMP ECHO REQUEST (no need to stop).
For each packet received, you will print the packet IP, packet sequence number, and time between the request and replay.
you can write your own code or modify the one  in the Moodle.
*In this part, handout ping.py code

### Watchdog timer - 40%
Watchdog is a timer to detect and recover your computer dis-functions or hardware fails. It’s a chip whose sole purpose is to receive a signal every millisecond from the CPU. It will reboot the system if it hasn’t received any signal for 10 milliseconds (mostly when hardware fails).
Modify the ping program, and write a watchdog that will hold a timer (TCP connection on port 3000) to ensure that if we don’t receive an ICMP-ECHO-REPLY after sending an ICMP-REQUEST for 10 seconds, it will exit and print "server <ip> cannot be reached."
Modify the ping.py program so that it will execute the watchdog.py program as well using threads.

*You don’t have to use threads. You can also use the fork(2) and exec(2) workflow for execution
*Note that every time ping.py sends a packet, it will need to update watchdog.py timer.
*It is required that the code will work on localhost on both ping.py and watchdog.py.
*In part b you will handout better_ping.py and watchdog.py

  ### run with "python def_better_ping.py" 
