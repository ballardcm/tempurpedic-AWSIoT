#!/usr/bin/python 

import socket

BED1_IP = "10.0.1.177"
BED2_IP = "10.0.1.178"

UDP_PORT = 50007

arg = 2

flat = "3305320A945C0400CC"
pos1 = "33053203945C0000C8"
pos2 = "33053203945C0100C9"
pos3 = "33053203945c0100CA"
pos4 = "33053203945c0100CB"

if arg == 1:
	bed_pos = pos1
elif arg == 2:
	bed_pos = pos2
elif arg == 3:
	bed_pos = pos3
elif arg == 4:
	bed_pos = pos4
else:
	bed_pos = flat


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(bed_pos.decode("hex"), (BED1_IP, UDP_PORT))
sock.sendto(bed_pos.decode("hex"), (BED2_IP, UDP_PORT))

