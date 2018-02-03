from .http_log_process import process_http_log
import os
import requests


def get_logfile_list(ctl_name):
    mac_log_dict = dict()
    for dir_name, dir_names, file_names in os.walk(ctl_name):
        files_with_log_extension = []
        for file in file_names:
            if file.endswith('.log'):
                files_with_log_extension.append(file)
        if len(files_with_log_extension) > 0:
            mac_log_dict[dir_name] = files_with_log_extension
    return mac_log_dict


def get_log_file_uri(mac_address, date_string, request_type):
    api_uri = 'http://54.193.126.147:3000/api/networkData/logFileData/'
    return api_uri + mac_address + '/' + date_string + '/' + request_type


def run_processing_log_files_of_all_directories():
    mac_log = get_logfile_list('/home/traffic/unctrl')
    # mac_http_dict = dict()

    for dir_name, log_name_list in mac_log.items():
        # http_data_dict = dict()
        mac_address = dir_name[21:]
        # mac_http_dict[mac_address] = http_data_dict
        for log_name in log_name_list:
            k = dir_name + '/' + log_name
            if str.startswith(log_name, 'https-'):
                request_type = 'https'
                date_string = log_name[len('https-'):-(len('log'))]
            elif str.startswith(log_name, 'http-'):
                request_type = 'http'
                date_string = log_name[len('http-'):-(len('log'))]
            else:
                raise ValueError("Invalid HTTP logfile, the file should start with 'http' or 'https'")

            http_log_list = process_http_log(k)
            if len(http_log_list) == 0:
                continue
            # http_data_dict[date_string] = http_log_list
            r = requests.post(get_log_file_uri(mac_address, date_string, request_type), json=http_log_list)