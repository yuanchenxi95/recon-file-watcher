from .http_log_process import process_http_log
import os


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


def run_processing_log_files_of_all_directories():
    mac_log = get_logfile_list('/home/traffic/unctrl')

    print(mac_log)
    # for dir_name, filename in mac_log.items():
    #     k = dir_name + '/' + filename
    #     mac_http_dict = dict()
    #     mac_http_dict["data"] = process_pcap(k)
    #     if len(mac_http_dict["data"]) == 0:
    #         continue
    #     mac_http_dict["id"] = dir_name[21:]
    #     r = requests.post("http://54.193.126.147:3000/api/networkData/todayData", json=mac_http_dict)
        # print(r.content)