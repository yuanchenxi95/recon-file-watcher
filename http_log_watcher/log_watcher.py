from .http_log_process import process_http_log
import os
import requests
import time
import logging
from datetime import datetime


REMOTE_HOST = 'http://ec2-54-193-126-147.us-west-1.compute.amazonaws.com:3000'
FEBRUARY_DATE_TIME = datetime(2018, 3, 1)

FILE_PATH = 'file_path'
LINE_NUMBER_PROCESSED = 'line_number_processed'
UPDATE_TIME = 'update_time'


def get_file_log(file_processing, file_path):
    return file_processing.find_one({ FILE_PATH: file_path })


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


def get_last_time_processed_line(file_log):
    if file_log is None:
        return 0
    return file_log[LINE_NUMBER_PROCESSED]


def check_last_update_time(file_log, last_update_time):
    if file_log is None:
        return True
    return float(last_update_time) > float(file_log[UPDATE_TIME])


def get_file_last_modified_time(file_path):
    return os.path.getmtime(file_path)


def write_http_log_data(http_data_query, http_log_list):
    http_data_query.insert_many(http_log_list)


def write_modified_data(file_processing_query, file_path, file_last_modified_time, this_time_line):
    new_log = {
        FILE_PATH: file_path,
        LINE_NUMBER_PROCESSED: this_time_line,
        UPDATE_TIME: file_last_modified_time
    }
    file_processing_query.update({
        FILE_PATH: file_path
    }, new_log, upsert=True)


def get_file_processing_collection(mongo_client):
    return mongo_client['py-file-processing-log']


def get_http_data_collection(mongo_client):
    from pymongo import TEXT
    http_data_collection = mongo_client['httpdatas']
    http_data_collection.create_index(
        [('src_ip', TEXT),
         ('dst_ip', TEXT),
         ('src_port', TEXT),
         ('dst_port', TEXT),
         ('host', TEXT),
         ('http_method', TEXT),
         ('time_stamp', TEXT)],
        unique=True)
    return http_data_collection


def run_processing_log_files_of_all_directories(mongo_client):
    file_processing_query = get_file_processing_collection(mongo_client=mongo_client)
    http_data_query = get_http_data_collection(mongo_client=mongo_client)
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

            parsed_datetime = datetime.strptime(date_string, "%Y-%m-%d")

            # skip the file before january
            if FEBRUARY_DATE_TIME > parsed_datetime:
                continue

            # check whether to process the file
            file_last_modified_time = get_file_last_modified_time(file_path)
            file_log = get_file_log(file_processing_query, file_path)
            last_time_line = get_last_time_processed_line(file_log)
            logging.info("processing file: " + file_path)
            logging.info("file_last_modified_time: " + str(file_last_modified_time))
            if check_last_update_time(file_log, file_last_modified_time):
                logging.info("process the file")
                http_log_list, this_time_line = process_http_log(file_path, last_time_line)
                write_modified_data(file_processing_query, file_path, file_last_modified_time, this_time_line)

                if len(http_log_list) == 0:
                    continue
                # http_data_dict[date_string] = http_log_list
                # requests.post(get_log_file_uri(mac_address, date_string, request_type), json=http_log_list)
                write_http_log_data(http_data_query, http_log_list)
            else:
                logging.info("skip the file")
                continue
