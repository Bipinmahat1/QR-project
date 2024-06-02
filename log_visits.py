import sqlite3
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

DATABASE = 'visits.db'

# Initialize the database
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS visits (id INTEGER PRIMARY KEY, source TEXT)''')
    conn.commit()
    conn.close()

# Log a visit to the database
def log_visit(source):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO visits (source) VALUES (?)', (source,))
    conn.commit()
    conn.close()

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url_parts = urlparse(self.path)
        if url_parts.path == "/redirect":
            query = parse_qs(url_parts.query)
            source = query.get('source', ['direct'])[0]
            log_visit(source)
            self.send_response(302)
            self.send_header('Location', 'https://vaskrneup.com/')
            self.end_headers()
        elif url_parts.path == "/dashboard":
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute('SELECT source, COUNT(*) FROM visits GROUP BY source')
            data = c.fetchall()
            conn.close()

            html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Dashboard</title>
            </head>
            <body>
                <h1>Visitor Analytics</h1>
                <table>
                    <tr>
                        <th>Source</th>
                        <th>Count</th>
                    </tr>
            '''
            for source, count in data:
                html += f'<tr><td>{source}</td><td>{count}</td></tr>'
            html += '''
                </table>
            </body>
            </html>
            '''
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    init_db()
    server = HTTPServer(('localhost', 8000), SimpleHandler)
    print("Server started at http://localhost:8000/dashboard")
    server.serve_forever()
