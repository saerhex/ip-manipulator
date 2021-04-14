from ipaddress import IPv4Address, IPv4Network


def bin_conv(string):
    if string == '-':
        return 'Can\'t convert!'
    return '{:#b}'.format(IPv4Address(string))[2:]


class Ip:
    def __init__(self, ip_addr):
        self._ip_addr = IPv4Address(ip_addr)

    def __int__(self):
        return int(self._ip_addr)

    def __str__(self):
        return str(self._ip_addr)

    def get_class(self):
        bin_repr = bin_conv(self._ip_addr)
        if bin_repr.startswith('0'):
            return 'A'
        if bin_repr.startswith('10'):
            return 'B'
        if bin_repr.startswith('110'):
            return 'C'
        if bin_repr.startswith('1110'):
            return 'D'
        if bin_repr.startswith('11110'):
            return 'E'

    def get_mask(self):
        masks = {
            'A': '255.0.0.0',
            'B': '255.255.0.0',
            'C': '255.255.255.0',
            'D': '-',
            'E': '-'
        }
        return masks.get(self.get_class())

    def get_net_addr(self):
        bin_mask = int(bin_conv(self.get_mask()), 2)
        bin_ip = int(bin_conv(self._ip_addr), 2)

        return str(IPv4Address(bin_ip & bin_mask))

    def get_host_addr(self):
        ip_cls = self.get_class()
        bin_ip = bin_conv(self._ip_addr)
        if ip_cls == 'A':
            return str(IPv4Address(int(bin_ip[8:])))
        if ip_cls == 'B':
            return str(IPv4Address(int(bin_ip[16:])))
        if ip_cls == 'C':
            return str(IPv4Address(int(bin_ip[24:])))
        else:
            return "No host address for ip!"


class CIDRIp:
    def __init__(self, ip_addr):
        self._ip_addr = IPv4Network(ip_addr)

    @staticmethod
    def get_dot_notation(ip_addr):
        return str(IPv4Network(ip_addr).with_netmask)

    @staticmethod
    def get_slash_notation(ip_addr):
        return str(IPv4Network(ip_addr).with_prefixlen)

    def get_broadcast(self):
        return str(self._ip_addr.broadcast_address)

    @staticmethod
    def get_hosts_range(ip_addr):
        hosts = list(IPv4Network(ip_addr).hosts())
        return f"{str(hosts[0])} - {str(hosts[-1])}"
