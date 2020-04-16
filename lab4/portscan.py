from scapy.config import conf
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr

__author__ = "nichil"
__date__ = "12.04.2020"
__github__ = "https://github.com/starvis"


def send_syn(ip, dport, iface):
    packages = IP(dst=ip, ttl=43) / TCP(dport=dport, flags='S')
    return sr(packages, timeout=2, iface=iface)


def main():
    # print(conf)
    # do not output anything from scapy
    conf.verb = False

    ip = '192.168.130.128'
    dport = 1, 1024
    iface = 'VMware Network Adapter VMnet8'

    open_ports = []

    print("Searching .. ")

    # port syntax is either single 443 or range (1, 1024)
    for i in range(dport[0], dport[1]):
        results, unanswered = send_syn(ip=ip, dport=i, iface=iface)
        for result in results:
            # get the response->[1] from sent packet->[0] and from the response get the 2nd tuple object
            tcp = result[1][1]
            # if syn and ack bits are set print the sourceport
            if tcp.flags == 'SA':
                open_ports.append(tcp.sport)

    print("Found open Ports:", open_ports)

    # for pout, pin in results:
    #     # only get packets with MF flag set
    #     if pin.getlayer('IP').flags & 2:
    #         print(pin.getlayer('TCP').sport)


if __name__ == "__main__":
    main()
