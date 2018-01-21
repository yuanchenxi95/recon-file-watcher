from pcap_process import process_pcap
import os

if __name__ == '__main__':
    # pcap_list = process_pcap('/Users/ChenxiYuan/Project/ReconFileWatcher/2017-12-08_19.00.02_192.168.10.131.pcap')
    # for pcap in pcap_list:
    #     print(pcap)
    mac_log_dict = dict()
    for dir_name, dir_names, file_names in os.walk('/home/traffic/unctrl'):
        # print path to all subdirectories first.
        files_with_log_extension = []
        for file in file_names:
            if file.endswith('.log'):
                files_with_log_extension.append(file)
        mac_log_dict[dir_name] = files_with_log_extension

    print(mac_log_dict)

