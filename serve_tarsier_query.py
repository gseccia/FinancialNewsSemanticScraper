from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import urllib.parse
import re
import financial_web_scraper

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        news = financial_web_scraper.retrieve_news()
        self.wfile.write(bytes("<html><head><title>Financial News</title></head>", "utf-8"))
        self.wfile.write(bytes("<html><head><title>List of Nesw taken from finviz.com</title></head>", "utf-8"))
        for n in news:
            self.wfile.write(bytes("<body><p>"+n+"</p>", "utf-8"))
        #self.wfile.write(bytes("<body><p>This is a test.</p>", "utf-8"))
        self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
    """
    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\nQuery:\n\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'),
                self._parse_query(post_data))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
    
    def _parse_query(self, post_data):
        query:str = urllib.parse.unquote(post_data.decode('utf-8'))
        query=query.replace("+"," ")
        start="query="
        end="&"
        query = (query.split(start))[1].split(end)[0]
        return query


def run(server_class=HTTPServer, handler_class=S, port=9000):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
    """
