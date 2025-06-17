import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)

print("Serveur en écoute sur http://localhost:8080")

while True:
    client_connection, address = server_socket.accept()
    print(f"Connexion reçue de {address}")
    
    request_data = client_connection.recv(1024)

    reponse = """HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 12
Connection: close

Hello World!"""
    
    client_connection.sendall(reponse.encode('utf-8'))
    
    client_connection.close()