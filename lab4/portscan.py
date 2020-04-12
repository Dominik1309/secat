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
    # enable debug log
    conf.logLevel = 10
    ip = '192.168.130.128'
    dport = 22
    sport = 53231
    iface = 'VMware Network Adapter VMnet8'

    # port syntax is either single 443 or range (1, 1024)
    results, unanswered = send_syn(ip=ip, dport=dport, iface=iface)

    print(results)

    for result in results:
        if result[1][1].flags == 'SA':
            print(result[1][1].sport)
    # for pout, pin in results:
    #     # only get packets with MF flag set
    #     if pin.getlayer('IP').flags & b'001':
    #         print(pin.getlayer('TCP').sport)


if __name__ == "__main__":
    main()
