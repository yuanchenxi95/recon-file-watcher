from pcap_process import process_pcap
import os

if __name__ == '__main__':
    # pcap_list = process_pcap('/Users/ChenxiYuan/Project/ReconFileWatcher/2017-12-08_19.00.02_192.168.10.131.pcap')
    # for pcap in pcap_list:
    #     print(pcap)
    mac_or_ip_addresses = []
    for dirname, dirnames, filenames in os.walk('/home/traffic/unctrl'):
        # print path to all subdirectories first.
        mac_or_ip_addresses.append(dirname)
        print(filenames)

    print(mac_or_ip_addresses)

