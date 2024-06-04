import json
import logging
import re
import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer
from antispoof import validate_image


class LocalData(object):
    records = {}


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if re.search('/api/post/*', self.path):
            length = int(self.headers.get('content-length'))
            data = self.rfile.read(length).decode('utf8')

            record_id = self.path.split('/')[-1]
            LocalData.records[record_id] = data

            logging.info("add record %s: %s", record_id, data)
            self.send_response(200)
        else:
            self.send_response(403)
        self.end_headers()

    def do_GET(self):
        if re.search('/main', self.path):
            self.path = 'index.html'
        elif re.search('/api/get/*', self.path):
            record_id = self.path.split('/')[-1]
            if record_id in LocalData.records:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()

                # Return json, even though it came in as POST URL params
                data = json.dumps(LocalData.records[record_id]).encode('utf-8')
                logging.info("get record %s: %s", record_id, data)
                self.wfile.write(data)

            else:
                self.send_response(404, 'Not Found: record does not exist')
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.path = 'index.html'
            file_to_open = open(self.path).read()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
            # self.send_response(200)
            # self.send_header('Content-Type', 'application/json')
            # self.end_headers()
            # data = json.dumps([1,2,3]).encode('utf-8')
            # self.wfile.write(data)
            # self.send_response(403)
        self.end_headers()

    def do_POST(self):
        if re.search('/check-image', self.path):
            
            form = cgi.FieldStorage(
            fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                        'CONTENT_TYPE': self.headers['Content-Type'],
                        }
            )
                
            id = form.getvalue("id")
            image = form.getvalue("image")
            print(id)
            
            predict, score = validate_image(image,'./resources/anti_spoof_models', 0)
            isReal = False
            if predict == 1:
                isReal = True
            print("predict :"+str(predict))
            print("score :"+str(score))

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            result = {
                'status': 200,
                'isReal': isReal,
                'score': score
            }

            data = json.dumps(result).encode('utf-8')
            self.wfile.write(data)

        
if __name__ == '__main__':
    print('mulai')
    server = HTTPServer(('localhost', 9000), HTTPRequestHandler)
    # logging.info('Starting httpd...\n')
    print('run server')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    print("close")
    server.server_close()
    # logging.info('Stopping httpd...\n')