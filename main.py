from pcap_process import process_pcap
from http_log_process import process_http_log
import os
import requests
import json

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

    ip_processed_data_dict = dict()
    for folder in mac_log_dict:
        for log_file in folder:
            ip_processed_data_dict[log_file] = process_http_log(log_file)
    print(ip_processed_data_dict)
    # r = requests.post("https://api.myjson.com/bins", )

