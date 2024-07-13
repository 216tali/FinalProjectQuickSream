import re
import socket
import subprocess

devs_list = None


def my_address():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.connect(("8.8.8.8", 80))

        ip_address = sock.getsockname()[0]
        return ip_address
    except socket.error as e:
        print(f"Error: {e}")
    finally:
        sock.close()


def find_devices():
    global devs_list
    devs = subprocess.run(['arp', '-a'], capture_output=True, text=True, check=True)
    devs_list = devs.stdout
    return devs_list


def find_specific_address(address):
    if devs_list is None:
        return False
    ip_addresses = re.findall(r'\d+\.\d+\.\d+\.\d+', devs_list)
    if address in ip_addresses:
        return True
    else:
        return False