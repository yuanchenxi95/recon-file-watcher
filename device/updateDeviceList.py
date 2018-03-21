if __name__ == '__main__':
    fname = '/home/traffic/devices.txt'
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    print(content)
