from .http_log_process import process_http_log
import os
import requests
import time
import logging


REMOTE_HOST = 'http://ec2-54-193-126-147.us-west-1.compute.amazonaws.com:3000'


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
    api_uri = REMOTE_HOST + '/api/networkData/logFileData/'
    return api_uri + mac_address + '/' + date_string + '/' + request_type


def get_last_time_processed_line(db, file_path):
    if file_path not in db['last_time_line']:
        return 0
    return db['last_time_line'][file_path]


def check_last_update_time(db, file_path, last_update_time):
    if file_path not in db['update_time']:
        return True
    return float(last_update_time) > float(db['update_time'][file_path])


def get_file_last_modified_time(file_path):
    return os.path.getmtime(file_path)


def write_modified_data(db, file_path, file_last_modified_time, this_time_line):
    db['update_time'][file_path] = file_last_modified_time
    db['last_time_line'][file_path] = this_time_line


def run_processing_log_files_of_all_directories(db):
    mac_log = get_logfile_list('/home/traffic/unctrl')
    # mac_http_dict = dict()

    for dir_name, log_name_list in mac_log.items():
        # http_data_dict = dict()
        mac_address = dir_name[21:]
        # mac_http_dict[mac_address] = http_data_dict
        for log_name in log_name_list:
            file_path = dir_name + '/' + log_name
            if str.startswith(log_name, 'https-'):
                request_type = 'https'
                date_string = log_name[len('https-'):-(len('.log'))]
            elif str.startswith(log_name, 'http-'):
                request_type = 'http'
                date_string = log_name[len('http-'):-(len('.log'))]
            else:
                raise ValueError("Invalid HTTP logfile, the file should start with 'http' or 'https'")

            # check whether to process the file
            file_last_modified_time = get_file_last_modified_time(file_path)
            last_time_line = get_last_time_processed_line(db, file_path)
            logging.info("processing file: " + file_path)
            logging.info("file_last_modified_time: " + str(file_last_modified_time))
            if check_last_update_time(db, file_path, file_last_modified_time):
                logging.info("process the file")
                http_log_list, this_time_line = process_http_log(file_path, last_time_line)
                write_modified_data(db, file_path, file_last_modified_time, this_time_line)

                if len(http_log_list) == 0:
                    continue
                # http_data_dict[date_string] = http_log_list
                # requests.post(get_log_file_uri(mac_address, date_string, request_type), json=http_log_list)
            else:
                logging.info("skip the file")
                continue
