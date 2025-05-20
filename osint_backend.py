# osint_backend.py
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class OSINTHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self._set_headers()
            self.wfile.write(json.dumps({"mensaje": "API OSINT funcionando"}).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == "/buscar":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
                return

            resultados = {
                "ANSES": "No se encontró información",
                "AFIP": "Resultado encontrado con coincidencias parciales",
                "NICAR": "Dominio registrado a nombre del titular",
                "SAIJ": "Sin registros judiciales disponibles",
                "ARBA": "Deuda registrada por $12.300",
                "TELÉFONO": "Número asociado a Juan Pérez, línea activa"
            }

            response = {"input": data, "resultados": resultados}
            self._set_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")


def run(server_class=HTTPServer, handler_class=OSINTHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servidor OSINT corriendo en puerto {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
