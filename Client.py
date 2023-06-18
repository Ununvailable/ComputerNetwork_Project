import socket


def client():
    host = '127.0.0.1'
    port = 5000

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout value for the socket
    client_socket.settimeout(1)

    sequence_number = 0
    packet_number = 0

    while True:
        # Create the packet with header bits (S, N, P)
        packet = str(sequence_number) + str(packet_number) + '0'  # Assuming all packets are valid

        # Send the packet to the server
        client_socket.sendto(packet.encode('utf-8'), (host, port))
        print('Sent packet {} to server'.format(packet_number))

        try:
            # Wait for the ACK from the server
            ack, server_address = client_socket.recvfrom(1024)
            ack = ack.decode('utf-8')

            # Extract the header bits (S, N, P) from the ACK
            s = int(ack[0])
            n = int(ack[1])
            p = int(ack[2])

            if s == sequence_number and n == 0 and p == 0:
                # ACK received for the current packet, move to the next sequence number and packet
                sequence_number = 1 - sequence_number
                packet_number += 1
            elif n == 1 and p == 0:
                # ACK received for the previous packet, retransmit the current packet
                print('Received ACK for the previous packet. Retransmitting packet {}'.format(packet_number))

        except socket.timeout:
            # Timeout occurred, retransmit the current packet
            print('Timeout occurred. Retransmitting packet {}'.format(packet_number))

    # Send the end of transmission packet
    packet = str(sequence_number) + str(packet_number) + '2'
    client_socket.sendto(packet.encode('utf-8'), (host, port))
    print('Sent end of transmission packet {}'.format(packet_number))

    client_socket.close()


if __name__ == '__main__':
    client()
