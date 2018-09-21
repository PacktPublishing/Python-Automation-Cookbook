import http.server
import time
import argparse

PORT = 8000

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='delay', type=float, default=0.5,
                        help='delay introduced for each request, in seconds')
    args = parser.parse_args()
    delay_time = args.delay

    class DelayServer(http.server.SimpleHTTPRequestHandler):

        def do_GET(self):
            # Produce an artificial delay on each request
            time.sleep(delay_time)
            super().do_GET()

    Handler = DelayServer

    server = http.server.ThreadingHTTPServer(('localhost', 8000), Handler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
