import json


class HttpLogData:
    def __init__(self, src_ip, dst_ip, src_port, dst_port, host, http_method, time_stamp):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.host = host
        self.http_method = http_method
        self.time_stamp = time_stamp


    def __repr__(self):
        return str(self)

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


def convert_bytes_string_regular_string(bytes_string):
    return str(bytes_string, 'utf-8')


def process_http_log(file_path):
    """Open up a test pcap file and print out the packets"""
    http_log_data_list = []
    with open(file_path, 'rb') as f:
        flag = True
        for line in f:
            if not flag:
                flag = True
                continue
            words = line.split()
            src_ip = convert_bytes_string_regular_string(words[2])
            dst_ip = convert_bytes_string_regular_string(words[4])
            src_port = convert_bytes_string_regular_string(words[3])
            dst_port = convert_bytes_string_regular_string(words[5])
            host = convert_bytes_string_regular_string(words[8])
            http_method = convert_bytes_string_regular_string(words[7])
            time_stamp = convert_bytes_string_regular_string(words[0])
            http_log_data = HttpLogData(src_ip, dst_ip, src_port, dst_port, host, http_method, time_stamp)
            http_log_data_list.append(http_log_data)
        return http_log_data_list
