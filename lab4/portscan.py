from scapy.config import conf
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr

__author__ = "nichil"
__date__ = "12.04.2020"
__github__ = "https://github.com/starvis"


def scan_tcp_port_range(ip, port):
    packages = IP(dst=ip, ttl=43) / TCP(dport=port)
    result = sr(packages, timeout=2)
    return result


def main():
    # print(conf)
    # enable debug log
    conf.logLevel = 10
    ip = '192.168.178.22'

    # port syntax is either single 443 or range (1, 1024)
    results, unanswered = scan_tcp_port_range(ip=ip, port=(5000, 10000))

    print(results)

    # for i in result:
    #     if i.listname == 'Results':
    #         print("Replies: ", len(i))
    #         for j in i:
    #             print(j)

    # for result in results:
    #     for layer in result:
    #         if layer.getlayer('IP').flags & 2:
    #             print(layer.getlayer('TCP').sport)

    for pout, pin in results:
        if pin.getlayer('IP').flags & 2:
            print(pin.getlayer('TCP').sport)


if __name__ == "__main__":
    main()
