import socket
from datetime import datetime

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)

print("Serveur en écoute sur http://localhost:8080")

while True:
    client_connection, address = server_socket.accept()
    print(f"Connexion reçue de {address}")
    
    request_data = client_connection.recv(1024).decode('utf-8')
    
    if not request_data:
        client_connection.close()
        continue

    premiere_ligne = request_data.splitlines()[0]
    chemin = premiere_ligne.split(' ')[1]
    
    if chemin == "/motd":
        corps = "Bienvenue chez CanaDuck !"
        status = "200 OK"
    elif chemin == "/date":
        now = datetime.now()
        corps = f"Nous sommes le {now.strftime('%A %d %B %Y, %H:%M:%S')}"
        status = "200 OK"
    else:
        corps = "Ressource non trouvee"
        status = "404 Not Found"

    reponse = f"""HTTP/1.1 {status}
Content-Type: text/plain
Content-Length: {len(corps)}
Connection: close

{corps}"""
    
    client_connection.sendall(reponse.encode('utf-8'))
    client_connection.close()