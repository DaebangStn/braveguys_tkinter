from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from urllib.parse import urlparse

class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path=urlparse(self.path)

        message_parts=['Client address : {0:s}'.format(self.client_address),
                       'Client string : {0:s}'.format(self.address_string()),
                       'Command : {0:s}'.format(self.command),
                       'Path : {0:s}'.format(self.path),
                       'real path : {0:s}'.format(parsed_path.path),
                       'query : {0:s}'.format(parsed_path.query),
                       'request version : {0:s}'.format(self.request_version),
                       'server_version : {0:s}'.format(self.server_version),
                       'sys_version : {0:s}'.format(self.sys_version),
                       'protocol_version : {0:s}'.format(self.protocol_version)]

        message='<br>'.join(message_parts)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))
        return None

s=HTTPServer(('localhost',8080), SimpleHTTPRequestHandler)
s.serve_forever()
