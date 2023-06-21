import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
SIZE = 1027
FORMAT = "utf-8"


def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[+] Listening...")

    conn, addr = server.accept()
    print(f"[+] Client connected from {addr[0]}:{addr[1]}")

    # Receive filename and filesize
    data = conn.recv(SIZE).decode(FORMAT)
    filename, filesize = data.split("_")
    filesize = int(filesize)

    print("[+] Filename and filesize received from the client.")
    conn.send("Filename and filesize received".encode(FORMAT))

    # Receive data packets and write to file
    packet_seq = 0  # Number of the current packet
    with open(f"recv_{filename}", "wb") as f:
        while True:
            data = conn.recv(SIZE)
            if not data:
                break

            # Extract packet sequence number from first 3 bits
            packet_num = int.from_bytes(data[:1], byteorder="big")

            # Extract the error of byte 5
            pdf_value = int.from_bytes(data[2:3], byteorder="big")
            pdf_value = int(pdf_value/100)
            if pdf_value > 0.35:
                error = 1
            else:
                error = 0
            # Check packet sequence number
            if packet_num != packet_seq or error == 1:
                print(f"Packet {packet_seq} sent is failed.. Resending")
                expected_packet = str(packet_seq)
                conn.send(expected_packet.encode(FORMAT))
                continue

            # Update packet sequence number
            if packet_seq <7:
                packet_seq += 1
            else:
                packet_seq=0

            # Write data to file
            f.write(data[3:])

            # Send confirmation message
            print(f"Packet {packet_num} sent is succesful")
            conn.send("Data received.".encode(FORMAT))

    print("File is sent successfully")
    conn.close()
    server.close()

if __name__ == "__main__":
    server()
