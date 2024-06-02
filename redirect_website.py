from http.server import HTTPServer, BaseHTTPRequestHandler

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Send a 302 (temporary) redirect response
        self.send_response(302)
        # Set the 'Location' header to the target website
        self.send_header('Location', 'https://vaskrneup.com/')
        self.end_headers()

def run_server():
    # Set up the server
    server_address = ('127.0.0.1', 8000)  # Listening on all available interfaces on port 8000
    httpd = HTTPServer(server_address, RedirectHandler)
    print('Server started at http://localhost:8000/redirect?source=qr')
    # Start serving indefinitely
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
