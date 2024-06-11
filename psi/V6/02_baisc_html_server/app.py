# Import the WSGI server module
import wsgiref.simple_server;

# This is the WSGI application callable
def application(environ, start_response):
    path = environ["PATH_INFO"];
    if path=="/":
        with open("index.html", "r") as f:
            response = f.read().encode();
        status = "200 OK";
    else:
        response = b"<h1>Not found</h1><p>Entered path not found</p>";
        status = "404 Not Found";

    headers = [
        ("Content-Type", "text/html"),
        ("Content-Length", str(len(response)))
    ];
    start_response(status, headers);
    return [response];

if __name__ == "__main__":
    w_s = wsgiref.simple_server.make_server(
        host="localhost",
        port=8021,
        app=application
    );
    w_s.handle_request();
# Server hostname
# Server port
# The WSGI application callable

# Handle a single HTTP request
