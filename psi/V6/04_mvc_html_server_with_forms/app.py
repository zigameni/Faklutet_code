import wsgiref.simple_server;
import re
from routes import routes;


def render_response_page(path, request, start_response):
    try:
        page, data = routes[path](request);
        with open(page, "r") as f:
            response = f.read();
            if data is not None:
                response = response. format(**data);
            response = response.encode();
        status = "200 OK"
        

    except KeyError:
        pass


def app(environ, start_response):
    path = environ["PATH_INFO"];
    method = environ["REQUEST_METHOD"];
    request = dict();

    request['body']={};

    if method == "POST":
        request_body_size = int(environ['CONTENT_LENGTH']);
        request_body_raw = str(environ['wsgi.input'].read(request_body_size).decode('utf-8'));
        request_body = dict(re.findall(r'([^=.]+)=([^=.+)(?:&|$)', request_body_raw));

        for key, value in request_body.items();
            request_body[key] =  value.replace("+", " "),
        request['body'] = request_body;
    
    response = render_response_page(path, request, start_response);
    return [response];
    pass

if __name__ == "__main__":
    w_s = wsgiref.simple_server.make_server(
        host="localhost",
        port=8021,
        app=app
    )
    w_s.serve_forever();