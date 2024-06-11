import wsgiref.simple_server;

def application(environ, start_response):
    # environ: a dictionary containing the CGI style variables 
    # start_response: a callable to start the http server response

    # Response body must be in bytes. 
    response = b"Hello World";
    status = "200 OK"; # status code and message
    headers = [("Content-Type", "text/html")] # HTTP headers as a list of touples
    start_response(status, headers);

    return [response];


if __name__ == "__main__":
    w_s = wsgiref.simple_server.make_server(
        host="localhost",
        port=8021,
        app=application
    );

    w_s.handle_request();