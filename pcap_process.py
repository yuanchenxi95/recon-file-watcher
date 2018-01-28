import dpkt
import datetime
import socket
from dpkt.compat import compat_ord
import json


class PcapDataClass:
    def __init__(self, eth_src_mac, eth_dst_mac, src_ip, dst_ip, header_host, http_method, time_stamp):
        self.eth_src_mac = eth_src_mac
        self.eth_dst_mac = eth_dst_mac
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.header_host = header_host
        self.http_method = http_method
        self.time_stamp = time_stamp

    def __repr__(self):
        return str(self)

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


def mac_addr(address):
    """Convert a MAC address to a readable/printable string
       Args:
           address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % compat_ord(b) for b in address)


def inet_to_str(inet):
    """Convert inet object to a string
        Args:
            inet (inet struct): inet network address
        Returns:
            str: Printable/readable IP address
    """
    # First try ipv4 and then ipv6
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)


def process_http_requests(f):
    pcap = dpkt.pcap.Reader(f)

    """Print out information about each packet in a pcap
       Args:
           pcap: dpkt pcap reader object (dpkt.pcap.Reader)
    """
    # For each packet in the pcap process the contents
    pcap_data_list = []
    for timestamp, buf in pcap:
        # Unpack the Ethernet frame (mac src/dst, ethertype)
        eth = dpkt.ethernet.Ethernet(buf)

        # Make sure the Ethernet data contains an IP packet
        if not isinstance(eth.data, dpkt.ip.IP):
            continue

        # Now grab the data within the Ethernet frame (the IP packet)
        ip = eth.data

        # Check for TCP in the transport layer
        if isinstance(ip.data, dpkt.tcp.TCP):

            # Set the TCP data
            tcp = ip.data

            # Now see if we can parse the contents as a HTTP request
            try:
                request = dpkt.http.Request(tcp.data)
            except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                continue

            # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
            do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
            more_fragments = bool(ip.off & dpkt.ip.IP_MF)
            fragment_offset = ip.off & dpkt.ip.IP_OFFMASK

            pcap_data_object = PcapDataClass(eth_src_mac=mac_addr(eth.src),
                                             eth_dst_mac=mac_addr(eth.dst),
                                             src_ip=inet_to_str(ip.src),
                                             dst_ip=inet_to_str(ip.dst),
                                             header_host=request.headers['host'],
                                             http_method=request.method,
                                             time_stamp=timestamp
                                             )
            pcap_data_list.append(pcap_data_object)
    return pcap_data_list


def process_pcap(file_path):
    """Open up a test pcap file and print out the packets"""
    with open(file_path, 'rb') as f:
        print(file_path)
        try:
            return_list = process_http_requests(file_path)
            print(return_list)
        except:
            return_list = []
        return return_list
