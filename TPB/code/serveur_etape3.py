from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

class MonHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            message = "Bonjour depuis BaseHTTPRequestHandler !"
            self.send_response(200)
        
        elif self.path == '/date':
            now = datetime.now()
            message = f"Nous sommes le {now.strftime('%A %d %B %Y, %H:%M:%S')}"
            self.send_response(200)
        
        else:
            self.send_error(404, "Ressource non trouvée")
            return

        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(message.encode('utf-8'))))
        
        self.end_headers()
        
        self.wfile.write(message.encode('utf--8'))


server_address = ('localhost', 8000)
httpd = HTTPServer(server_address, MonHandler)

print("Serveur actif sur http://localhost:8000")
httpd.serve_forever()