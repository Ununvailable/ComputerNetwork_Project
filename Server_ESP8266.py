import socket
import json
import serial


# IP address and port of the server
SERVER_IP = '0.0.0.0'  # Use 0.0.0.0 to listen on all available interfaces
SERVER_PORT = 8000  # Choose a port number
PACK_SIZE = 512
# PACK_SIZE = 1024


def main():
    # Initialize serial port for streaming IP address
    # ser = serial.Serial('COM5', 115200)

    # sendIP = socket.gethostbyname(socket.gethostname())
    # print(sendIP)

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the IP address and port
    server_socket.bind((SERVER_IP, SERVER_PORT))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Listening on {SERVER_IP}:{SERVER_PORT}")

    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    while True:
        # Constantly stream the IP address
        # ser.write(sendIP.encode())

        # Receive data from the client
        package = client_socket.recv(PACK_SIZE).decode('utf-8').strip('\n')

        print(f"Received data: {package}")
        print(f"Size of package: {len(package)}")
        # Process the received data (e.g., perform some action or validation)
        header = package[0]
        json_string = package[1:]
        print(f"Header: {header}, type: {type(header)}")
        print(f"JSON string: {json_string}")

        # Send ACK back to the client
        ack_message = header
        client_socket.sendall(ack_message.encode('utf-8'))
        print(f"Sent ACK to client, {ack_message}")

        # Close the client socket connection
        # server_socket.close()
        print("\n")


if __name__ == "__main__":
    main()
