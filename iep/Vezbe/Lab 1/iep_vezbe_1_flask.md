# Flask, IEP vezbe 1

## Overview

- **Web Framework**
- Created by **Amin Ronacher**
- Combines **Werkzeug WSGI toolkit** and **Jinja2 template engine**
- Often called a **micro framework**
  - Does not include modules for database communication, data validation, etc., but these can be added as needed.

## Flask – Minimal Application

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
```

### Setup

```bash
python -m venv ./venv
./venv/Scripts/activate
pip install flask
python script.py
```

## Flask Application Object

- **WSGI application** represented by the Flask class object
- **`app.route(rule, options)`**: Decorator for binding functions to a URL
  - **rule**: URL address for the function
  - **options**: Additional parameters (e.g., HTTP methods)
- **`app.run(host, port, debug, options)`**: Starts the application
  - **host**: Address for accessing the application (default is 127.0.0.1; 0.0.0.0 makes it externally accessible)
  - **port**: Port for accessing the application (default is 5000)
  - **debug**: Whether the app runs in debug mode (immediate code change visibility)
  - **options**: Additional parameters for the Werkzeug server

## Routing in Flask

### Basic Routing

```python
@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'
```

### Note

- Accessing `localhost/hello/` and `localhost/about/` produces a 404 error.
- Accessing `localhost/projects` and `localhost/projects/` leads to the `projects` function.

### Routing with Blueprints

```python
from flask import Blueprint

bp = Blueprint("foo", __name__, url_prefix="foo")

@bp.route("/bar")
def bar():
    return "bar"

from flask import Flask
app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
```

### Nested Blueprints

```python
parent = Blueprint('parent', __name__, url_prefix='/parent')
child = Blueprint('child', __name__, url_prefix='/child')

parent.register_blueprint(child)
app.register_blueprint(parent)

url_for('parent.child.create')  # /parent/child/create
```

### Path Parameters

```python
from markupsafe import escape

@app.route('/user/<forename>/<surname>')
def show_user_profile(forename, surname):
    return f'User {escape(forename)} {escape(surname)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'Subpath {escape(subpath)}'
```

### Converters

- **string**: Default, accepts any text without a slash
- **int**: Accepts positive integers
- **float**: Accepts positive floating point values
- **path**: Like string, but also accepts slashes
- **uuid**: Accepts UUID strings

## Flask – Request Object

### Attributes

- **args**: Query string parameters
- **json**: Request body in JSON
- **files**: Uploaded files
- **method**: HTTP method (GET, POST, PUT, etc.)

### Example:

```python
from flask import request

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        ...
    else:
        ...
    return "SUCCESS"
```

### Handling Files

```python
@app.route("/upload", methods=["POST"])
def upload():
    content = request.files["file"].stream.read()
    return content.decode()
```

#### Configuration for File Uploads

```python
app.config['UPLOAD_FOLDER'] = 'path/to/upload/folder'
app.config['MAX_CONTENT_PATH'] = 'maximum size in bytes'
```

## Flask – Response Object

- Represented by the **Response** class
- Can be created using **make_response** function

### Example

```python
from flask import make_response

@app.route(...)
def foo():
    r = make_response(...)
    r.headers['X-Something'] = 'A value'
    return r
```

### Automatic Conversion

- **Response object**: Returned directly
- **String**: Creates a Response object with status code 200
- **Iterator/Generator**: Treated as a data stream
- **Dictionary/List**: Converted to JSON using **jsonify**
- **Tuple**: Must be in the form of `(response, status)`, `(response, headers)`, or `(response, status, headers)`

## Flask – Application Configuration

### Methods to Set Configuration Variables:

- Direct assignment to **config** attribute
- Environment variables
- Configuration files
- Python classes

### Example

```python
app.config.from_object('yourapplication.default_settings')
```

## Flask – Application and Request Contexts

- Contexts are created and destroyed with each request
- Access via **current_app** and **request** global variables
- Manual context creation when needed outside request handling

### Example

```python
app = Flask(__name__)

with app.app_context():
    init_db()
```

## Flask – Logging

- Uses the **logging** module
- Default configuration only logs **warning** and above

### Example

```python
@app.route('/login', methods=['POST'])
def login():
    user = get_user(request.form['username'])
    if user.check_password(request.form['password']):
        login_user(user)
        app.logger.info('%s logged in successfully', user.username)
        return redirect(url_for('index'))
    else:
        app.logger.info('%s failed to log in', user.username)
        abort(401)
```

### Custom Logging Configuration

```python
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
```

## Flask – Sessions

- HTTP is a stateless protocol
- Session information is stored for user-related data

### Example

```python
from flask import session

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
    <form method="post">
        <p><input type=text name=username>
        <p><input type=submit value=Login>
    </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
```

## Task

- Create a simple web application for adding and searching employee data:
  - Store name, surname, email, gender, language spoken, and position for each employee
  - Allow adding individual employees and via CSV file
  - Enable search functionality for all attributes

### Testing

- The application can be tested using the **Postman** tool
