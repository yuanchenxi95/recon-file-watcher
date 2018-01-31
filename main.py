from pcap_process import process_pcap
from http_log_process import process_http_log
import os
import json
import requests
import time
import datetime
import schedule
import logging


def convert_date_string_to_time_stamp(pcap_name):
    return time.mktime(datetime.datetime.strptime(pcap_name[:10], "%Y-%m-%d").timetuple())


def find_the_latest_pcap_file(pcaps_list):
    return max(pcaps_list, key=convert_date_string_to_time_stamp)


def process_latest_pcap(ctl_name):
    mac_log_dict = dict()
    for dir_name, dir_names, file_names in os.walk(ctl_name):
        # print path to all subdirectories first.
        files_with_pcap_extension = []
        for file in file_names:
            if file.endswith('.pcap'):
                files_with_pcap_extension.append(file)
        if len(files_with_pcap_extension) > 0:
            mac_log_dict[dir_name] = find_the_latest_pcap_file(files_with_pcap_extension)
    return mac_log_dict


def run_processing_today_pcap():
    mac_log = process_latest_pcap('/home/traffic/unctrl')
    logging.info('-----------------------------------')
    logging.info(str(datetime.datetime.now))

    for dir_name, filename in mac_log.items():
        k = dir_name + '/' + filename
        mac_http_dict = dict()
        mac_http_dict["data"] = process_pcap(k)
        mac_http_dict["id"] = dir_name[21:]
        r = requests.post("http://54.193.126.147:3000/api/networkData/todayData", json=mac_http_dict)
        logging.info(mac_http_dict["id"] + " status: " + r.content)
        # print(r.content)


if __name__ == '__main__':
    schedule.every(1).minutes.do(run_processing_today_pcap)
    logging.basicConfig(filename='run_status.log', level=logging.DEBUG)
    while 1:
        schedule.run_pending()
        time.sleep(1)

    # print(mac_http_dict)
    # ip_processed_data_dict = dict()
    # for folder in mac_log_dict:
    #     for log_file in mac_log_dict[folder]:
    #         ip_processed_data_dict[folder] = process_http_log(folder + '/' + log_file)
    #
    # # print(ip_processed_data_dict)
    # with open('http.json', 'w') as f:
    #     f.write(str(ip_processed_data_dict))
