import socket
import threading
import pyautogui
import cv2
import numpy as np
import pickle
import re
from screenshot import capture_screen
from addresses import find_devices, find_specific_address


current_devs = None


def run_clients(connection, address):
    global current_devs
    current_devs = find_devices()
    if find_specific_address(address):
        print(f"Connection from {address}")

        try:
            while True:
                screen = capture_screen()
                data = pickle.dumps(screen)
                data_size = len(data)

                connection.sendall(data_size.to_bytes(4, 'big'))
                connection.sendall(data)

        except Exception as e:
            print(f"Error with client {address}: {e}")
        finally:
            connection.close()

    else:
        print(f"A client from another network tried to connect from the address:{address}")


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(39)  #המספר המקסימלי המותר לתלמידים בכיתה בישראל- 39
    print(f"Listening on {host}:{port}")

    try:
        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=run_clients, args=(conn, addr[0]))
            client_thread.start()
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()


start_server('0.0.0.0', 8820)

