import socket
import pickle
import cv2
from screenshot import capture_screen
from addresses import my_address

current_devs = None


def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")

    try:
        while True:
            data_bytes_amount = client_socket.recv(4)
            if not data_bytes_amount:
                break
            data_size = int.from_bytes(data_bytes_amount, 'big')
            data_sent = b""
            while len(data_sent) < data_size:
                packet = client_socket.recv(data_size - len(data_sent))
                if not packet:
                    break
                data_sent += packet

            if len(data_sent) != data_size:
                print(
                    f"Error: The data size received ({len(data_sent)}) does not match expected the data size ({data_size})")
                break

            screen = pickle.loads(data_sent)
            cv2.imshow("Screen", screen)
            if cv2.waitKey(1) & 0xFF == 27:  #27- הערך ASCII של המקש Escape במקלדת
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        cv2.destroyAllWindows()


start_client(my_address(), 8820)
