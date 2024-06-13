# JWT and Authorization Notes

## JWT (JSON Web Token)

### Overview

JWT is a string consisting of three parts: Header, Payload (data), and Signature.

- On the server, every incoming request first checks if the token is valid. This is done by re-encrypting the received data with the same key and verifying it against the signature.

### Token Parts

1. **Header**: Contains the algorithm used for signing the token (e.g., HS256) and the type of token.
2. **Payload**: Contains the claims or the data that we need for processing.
3. **Signature**: Ensures that the token is not tampered with.

### Standard JWT Fields

- `iat` (Issued At): Timestamp when the token was created.
- `nbf` (Not Valid Before): Token is not valid before this timestamp.
- `exp` (Expires At): Timestamp when the token expires.

### Example Configuration

```python
class Configuration:
    JWT_SECRET_KEY = "your_secret_key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
```

### Token Workflow

1. **Login**: Verify user credentials and issue a token.
2. **Token Validation**: On each request, validate the token by decrypting it and verifying the signature.
3. **Refresh Token**: Use the refresh token to issue a new access token.

### JWT with Flask

```python
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from datetime import timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    username = request.json.get('username', None)
    user = User.query.filter_by(email=email, username=username).first()
    if not user:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity={'email': email, 'username': username})
    return jsonify(access_token=access_token)

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)
```

## Roles and Authorization

Roles are used to determine which parts of the system a user can access, i.e., what access rights they have.

- **Linking Table**: Contains foreign keys for users and roles.
- **Groups**: Users can be grouped and assigned access rights as a group.

### User Registration

When implementing authentication, the system must have data received from users during registration. Registration assigns roles to users.

### Example: Login and Role Check

```python
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from functools import wraps

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    # Assume user authentication is done here
    access_token = create_access_token(identity={"email": email, "roles": ["admin", "user"]})
    return jsonify(access_token=access_token)

def role_check(role):
    def decorator(function):
        @wraps(function)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if role in claims['roles']:
                return function(*args, **kwargs)
            else:
                return jsonify({"msg": "Invalid role"}), 403
        return wrapper
    return decorator

@app.route('/admin', methods=['GET'])
@role_check('admin')
def admin_endpoint():
    return jsonify({"msg": "Welcome, admin!"})

if __name__ == '__main__':
    app.run()
```

## Decorators

Decorators in Python allow you to wrap a function and modify its behavior. They are useful for extending functionality without modifying the original function code.

### Basic Decorator Example

```python
def dashes_decorator(func):
    def wrapper():
        result = func()
        return "*****" + str(result) + "*****"
    return wrapper

@dashes_decorator
def say_hello():
    return "Hello"
```

### Decorator with Arguments

```python
def decorator_with_an_argument(argument):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return str(argument) + str(result) + str(argument)
        return wrapper
    return decorator

@decorator_with_an_argument(">>>")
def greet(name):
    return f"Hello, {name}"
```

### Using Flask JWT Decorators

```python
from flask_jwt_extended import jwt_required

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({"msg": "You are logged in!"})
```

## Handling Tokens and User Sessions

- **Invalid Tokens**: Ensure services are notified when a token is no longer valid.
- **Session Management**: Handle user sessions efficiently, especially in cases of horizontal scaling.

### Example of Session Invalidity Check

```python
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        # Additional checks can be added here
        return func(*args, **kwargs)
    return wrapper

@app.route('/secure-data', methods=['GET'])
@token_required
def secure_data():
    return jsonify({"msg": "This is secure data"})
```

## Summary

- **JWT**: Consists of header, payload, and signature for secure communication.
- **Roles and Authorization**: Manage access rights efficiently.
- **Decorators**: Enhance functions without modifying their core logic.
- **Session Management**: Ensure efficient handling of user sessions and token validity.
