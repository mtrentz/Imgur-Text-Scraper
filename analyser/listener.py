from http.server import HTTPServer, BaseHTTPRequestHandler
from ocr import detect_text
from database import insert_text
from http import HTTPStatus
from PIL import Image
import sqlite3
import json
import sys
import os

# Got the code from this comment https://gist.github.com/nitaku/10d0662536f37a087e1b#gistcomment-3375622
# which got it from somewhere else
class _RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(HTTPStatus.OK.value)
        self.send_header('Content-type', 'application/json')
        # Allow requests from any origin, so CORS policies don't
        # prevent local development.
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_POST(self):
        # Reads message
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        # Reply back
        self._set_headers()
        self.wfile.write(json.dumps({'success': True}).encode('utf-8'))

        # Get image name
        img_name = message['msg']

        HERE = os.path.dirname(sys.argv[0])

        # Image/File info
        img_identifier = img_name.split('.')[0]
        img_extension = img_name.split('.')[1]
        img_path = os.path.join(HERE, '..', 'imgs', img_name)

        # Conect do Database
        conn = sqlite3.connect(os.path.join(HERE, '..', 'detected_text.db'))
        c = conn.cursor()

        # Detects text
        text = detect_text(img_path)
        print(text)

        # Add text to DB
        insert_text(conn, c, img_identifier, img_extension, text)

        # Closes db connection
        conn.close()
    

    def do_OPTIONS(self):
        # Send allow-origin header for preflight POST XHRs.
        self.send_response(HTTPStatus.NO_CONTENT.value)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.send_header('Access-Control-Allow-Headers', 'content-type')
        self.end_headers()


def run_server():
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, _RequestHandler)
    print('serving at %s:%d' % server_address)
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()

    # POST with cURL
    # curl -d '{"msg":"test_msg"}' -X POST localhost:8001
    # curl -d '{"msg":"IgnUjr.png"}' -X POST localhost:8001