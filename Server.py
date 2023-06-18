import socket


def server():
    host = '127.0.0.1'
    port = 5000

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))

    print('Server listening on {}:{}'.format(host, port))

    expected_sequence_number = 0

    while True:
        # Receive data from the client
        data, client_address = server_socket.recvfrom(1024)
        data = data.decode('utf-8')

        # Extract the header bits (S, N, P)
        s = int(data[0])
        n = int(data[1])
        p = int(data[2])

        if s == expected_sequence_number and p == 0:
            # Packet is in order, send ACK
            ack = str(expected_sequence_number) + str(0) + str(0)  # S=expected_sequence_number, N=0, P=0
            server_socket.sendto(ack.encode('utf-8'), client_address)
            print('Received packet {} from client. Sent ACK {}'.format(expected_sequence_number, ack))

            expected_sequence_number = 1 - expected_sequence_number  # Flip the sequence number

        elif p == 1:
            # Packet is corrupted, request retransmission
            ack = str(1 - expected_sequence_number) + str(1) + str(0)  # S=previous_sequence_number, N=1, P=0
            server_socket.sendto(ack.encode('utf-8'), client_address)
            print('Received corrupted packet. Sent ACK {}'.format(ack))

        elif s == expected_sequence_number and p == 2:
            # End of transmission, break the loop
            print('End of transmission. Exiting...')
            break

    server_socket.close()


if __name__ == '__main__':
    server()
