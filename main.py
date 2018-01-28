from pcap_process import process_pcap
from http_log_process import process_http_log
import os
import json
import requests

if __name__ == '__main__':
    mac_log_dict = dict()
    for dir_name, dir_names, file_names in os.walk('/home/traffic/unctrl'):
        # print path to all subdirectories first.
        files_with_pcap_extension = []
        for file in file_names:
            if file.endswith('.pcap'):
                files_with_pcap_extension.append(file)
        mac_log_dict[dir_name] = files_with_pcap_extension

    print(mac_log_dict)
    # ip_processed_data_dict = dict()
    # for folder in mac_log_dict:
    #     for log_file in mac_log_dict[folder]:
    #         ip_processed_data_dict[folder] = process_http_log(folder + '/' + log_file)
    #
    # # print(ip_processed_data_dict)
    # with open('http.json', 'w') as f:
    #     f.write(str(ip_processed_data_dict))
