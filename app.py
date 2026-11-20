import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("bearer-logger")


class Handler(BaseHTTPRequestHandler):
    def _handle(self):
        auth = self.headers.get("Authorization", "")
        if auth.lower().startswith("bearer "):
            log.info("%s %s bearer_token=%s", self.command, self.path, auth[7:].strip())
            status, body = 200, b"token received\n"
        else:
            log.info("%s %s no bearer token", self.command, self.path)
            status, body = 401, b"missing bearer token\n"
        self.send_response(status)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    do_GET = do_POST = do_PUT = do_DELETE = _handle

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    log.info("listening on %d", port)
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
