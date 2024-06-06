import socket
import threading

def handle_client(client_socket):
    # Connect to the target server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(('127.0.0.1', 5001))

    while True:
        # Receive data from the client
        client_data = client_socket.recv(4096)
        if len(client_data) == 0:
            break

        # Forward the data to the server
        server_socket.sendall(client_data)

        # Receive data from the server
        server_data = server_socket.recv(4096)
        if len(server_data) == 0:
            break

        # Forward the data to the client
        client_socket.sendall(server_data)

    # Close the connections
    client_socket.close()
    server_socket.close()

def start_proxy():
    # Create a socket for the proxy server
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(('127.0.0.1', 8080))
    proxy_socket.listen(5)

    while True:
        # Accept client connections
        client_socket, client_address = proxy_socket.accept()
        print(f'Accepted connection from {client_address[0]}:{client_address[1]}')

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

start_proxy()