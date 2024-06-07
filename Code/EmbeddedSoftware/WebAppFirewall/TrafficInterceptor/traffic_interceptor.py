import socket
from collections import deque

# Define the host and port to listen on
HOST = 'localhost'
PORT = 8080

# Create a FIFO queue to store the captured web traffic
traffic_queue = deque()

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen()

    print(f"Listening on {HOST}:{PORT}...")

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()

        print(f"Connected to {client_address[0]}:{client_address[1]}")

        # Receive the incoming data
        data = client_socket.recv(4096)

        # Store the captured web traffic in the FIFO queue
        traffic_queue.append(data)

        # Process the received data (you can add your own logic here)

        # Send a response back to the client (optional)
        response = b"HTTP/1.1 200 OK\r\nContent-Length: 12\r\n\r\nHello World!"
        client_socket.sendall(response)

        # Close the client connection
        client_socket.close()