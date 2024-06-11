import wsgiref.simple_server
import re

routes = {
    '/': "index.html",
    '/results': "results.html"
}


def application(environ, start_response):
    path = environ["PATH_INFO"]
    method = environ["REQUEST_METHOD"]
    print(environ)
    if method == "POST":
        request_body_size = int(environ['CONTENT_LENGTH'])
        request_body_raw = environ['wsgi.input'].read(request_body_size).decode('utf-8')
        print(request_body_raw)
        request_body = dict(re.findall(r'([^=.]+)=([^=.]+)(?:&|$)', request_body_raw))
        print(request_body)
    try:
        print(path);
        print(routes[path]);
        with open(routes[path], "r") as f:
            response = f.read()
            if path != "/":
                print("We got here!");
                data = dict();
                data["proizvod"] = request_body['proizvodi']
                data["num"] = request_body['broj']
                response = response.format(**data);
            response = response.encode()
        status = "200 OK"
    except KeyError:
        response = b"<h1>Not Found</h1><p>Entered path not found</p>"
        status = "404 Not Found"
    headers = [
        ("Content-Type", "text/html"),
        ("Content-Length", str(len(response)))  # Corrected typo here
    ]
    start_response(status, headers)
    return [response]


if __name__ == '__main__':
    w_s = wsgiref.simple_server.make_server(
        host="localhost",
        port=8021,
        app=application
    )
    w_s.serve_forever()
