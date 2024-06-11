import traceback
import urllib.parse
import wsgiref.simple_server
import re
from routes import routes


def render_response_page(path, request, start_response):
    cookie_output = []
    try:
        page, data, cookie_output = routes[path](request)
        with open(page, "r") as f:
            response = f.read()
            if data is not None:
                response = response.format(**data)
            response = response.encode()
        status = "200 OK"
    except KeyError:
        traceback.print_exc()
        response = b"<h1>Not Found</h1><p>Entered path not found</p>"
        status = "404 Not Found"
    headers = [
        ("Content-Type", "text/html"),
        ("Content-Legth", str(len(response))),
    ]
    for output in cookie_output:
        headers.append(
            ("Set-Cookie", output)
        )
    start_response(status, headers)
    return response


def application(environ, start_response):
    path = environ["PATH_INFO"]
    method = environ["REQUEST_METHOD"]
    print(environ)
    request = dict()
    request['body'] = {}
    if method == "POST":
        request_body_size = int(environ['CONTENT_LENGTH'])
        request_body_raw = str(environ['wsgi.input'].read(request_body_size).decode('utf-8'))
        print(request_body_raw)
        request_body = dict(re.findall(r'([^=.]+)=([^=.]+)(?:&|$)', request_body_raw))
        for key, value in request_body.items():
            print(value)
            request_body[key] = value.replace("+", " ")
        request['body'] = request_body
    if "HTTP_COOKIE" in environ:
        request['cookies'] = environ["HTTP_COOKIE"]
    else:
        request['cookies'] = {}
    response = render_response_page(path, request, start_response)
    return [response]


if __name__ == '__main__':
    w_s = wsgiref.simple_server.make_server(
        host="localhost",
        port=8021,
        app=application
    )
    w_s.serve_forever()
