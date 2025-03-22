from scapy.all import *

pkts = sniff(iface='TP-Link Wireless USB Adapter', filter='tcp[tcpflags] == 2', prn=lambda x:x.summary())