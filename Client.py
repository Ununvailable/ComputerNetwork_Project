import os
import socket
from random import randrange
import numpy as np
from scipy.stats import norm

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
SIZE = 1029
FORMAT = "utf-8"
FILENAME = input("File name need to be sent is : ")
FILESIZE = os.path.getsize(FILENAME)

# Calcualte pdf by normal distribution
MU = 0.1
SIGMA = 0.05


def client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    # Send filename and filesize to server
    data = f"{FILENAME}_{FILESIZE}"
    client.send(data.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"SERVER: {msg}")

    with open(FILENAME, "rb") as f:
        packet_seq = 0  # packet sequence number
        while True:
            data = f.read(SIZE - 5)  # read a chunk of data, leave space for 3-byte sequence number
            if not data:  # the transmission is complete
                break

            random_val = np.random.randn()
            pdf_value = norm.pdf(random_val, 0.2, 1)

            pdf_value = int(pdf_value * 100)
            # prepend 3-byte sequence number to data
            packet = (packet_seq + randrange(0, 2)).to_bytes(3, byteorder="big") + b"\x00" + pdf_value.to_bytes(1, byteorder="big") + data

            # send packet to server and wait for confirmation
            while True:
                client.send(packet)
                msg = client.recv(SIZE).decode(FORMAT)
                if msg == "Data received.":
                    print(f"Packet {packet_seq} sent successfully.")
                    break
                else:
                    expected_seq = int(msg.split()[0])
                    print(f"Packet {packet_seq} fails to send. Resending...")
                    packet = expected_seq.to_bytes(3,
                                                   byteorder="big") + b"\x00\x00" + data  # prepend 3-byte sequence number to data

            # Update packet sequence number
            # if packet_seq <7:
            packet_seq += 1
            # else:
            # packet_seq=0

    print("File sent successfully.")
    client.close()


if __name__ == "__main__":
    client()
