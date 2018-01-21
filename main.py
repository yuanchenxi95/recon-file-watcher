from pcap_process import process_pcap

if __name__ == '__main__':
    pcap_list = process_pcap('/Users/ChenxiYuan/Project/ReconFileWatcher/2017-12-08_19.00.02_192.168.10.131.pcap')
    for pcap in pcap_list:
        print(pcap)