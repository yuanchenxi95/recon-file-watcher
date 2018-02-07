import json


def generate_http_dict(src_ip, dst_ip,src_port, dst_port, host, http_method, time_stamp):
    http_dict = dict()
    http_dict["src_ip"] = src_ip
    http_dict["dst_ip"] = dst_ip
    http_dict["src_port"] = src_port
    http_dict["dst_port"] = dst_port
    http_dict["host"] = host
    http_dict["http_method"] = http_method
    http_dict["time_stamp"] = time_stamp
    return http_dict


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


def process_http_log(file_path, line_number_should_skipped):
    """Open up a test pcap file and print out the packets"""
    http_log_data_list = []
    line_count = 0

    with open(file_path, 'rb') as f:
        # skip the processed_lines
        for line in f:
            line_count += 1
            if line_number_should_skipped == 0 or line_count <= line_number_should_skipped:
                continue

            words = line.split()
            src_ip = convert_bytes_string_regular_string(words[2])
            dst_ip = convert_bytes_string_regular_string(words[4])
            src_port = convert_bytes_string_regular_string(words[3])
            dst_port = convert_bytes_string_regular_string(words[5])
            host = convert_bytes_string_regular_string(words[8])
            http_method = convert_bytes_string_regular_string(words[7])
            time_stamp = convert_bytes_string_regular_string(words[0])
            http_log_data = generate_http_dict(src_ip=src_ip,
                                               dst_ip=dst_ip,
                                               src_port=src_port,
                                               dst_port=dst_port,
                                               host=host,
                                               http_method=http_method,
                                               time_stamp=time_stamp)
            http_log_data_list.append(http_log_data)
        return http_log_data_list, line_count
