import requests

HOST_URL = 'https://moniotr-smart-router-server.herokuapp.com/'

if __name__ == '__main__':
    fname = '/home/traffic/devices.txt'
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    deviceList = []
    for row in content:
        dataRow = row.split()
        deviceList.append({
            'mac_address': dataRow[0],
            'alias': dataRow[1]
        })
    print(deviceList)
    r = requests.post(HOST_URL + 'api/device/updateDeviceList', json=deviceList)
    print(r.content)

