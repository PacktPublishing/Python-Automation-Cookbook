import http.server
import time

PORT = 8000


class DelayServer(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        time.sleep(2)
        super().do_GET()


Handler = DelayServer

if __name__ == '__main__':
    server = http.server.ThreadingHTTPServer(('localhost', 8000), Handler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
# with socketserver.TCPServer(("", PORT), Handler) as httpd:
#     print("serving at port", PORT)
#     httpd.serve_forever()
