from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from urllib.parse import urlparse


mystatus = 'close'

class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        global mystatus
        print(mystatus)

        if self.path.endswith('/open'):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            mystatus = 'open'
            self.end_headers()
    
        elif self.path.endswith('/close'):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            mystatus = 'close'
            self.end_headers()
    
        elif self.path.endswith('/req'):
            if mystatus == 'open':
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
            else:
                self.send_response(404)
            
            self.end_headers()
        else:
            SimpleHTTPRequestHandler.do_GET(self)

        return None


if __name__ == "__main__":
    s=HTTPServer(('localhost',8080), MyHandler)
    s.serve_forever()
