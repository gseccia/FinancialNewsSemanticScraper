from http.server import BaseHTTPRequestHandler, HTTPServer
import time

import financial_web_scraper

hostName = "localhost"
hostPort = 9000

class LodLiveServer(BaseHTTPRequestHandler):

    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


        news = financial_web_scraper.retrive_news()
        self.wfile.write(bytes("<html><head><title>Financial News</title></head>", "utf-8"))
        self.wfile.write(bytes("<html><head><title>List of Nesw taken from finviz.com</title></head>", "utf-8"))
        for n in news:
            self.wfile.write(bytes("<body><p>"+n+"</p>", "utf-8"))
        #self.wfile.write(bytes("<body><p>This is a test.</p>", "utf-8"))
        self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
    """
    def do_GET(self):
        
        request_path = self.path
        
        print("\n----- Request Start ----->\n")
        print(request_path)
        print(self.headers)
        print("<----- Request End -----\n")
        
        self.send_response(200)
        self.send_header("Set-Cookie", "foo=bar")
        
    def do_POST(self):
        
        request_path = self.path
        
        print("\n----- Request Start ----->\n")
        print(request_path)
        
        request_headers = self.headers
        content_length = request_headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0
        
        print(request_headers)
        print(self.rfile.read(length))
        print("<----- Request End -----\n")
        
        self.send_response(200)
    
    do_PUT = do_POST
    do_DELETE = do_GET
    """

lod_server = HTTPServer((hostName, hostPort), LodLiveServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    lod_server.serve_forever()
except KeyboardInterrupt:
    pass

lod_server.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))