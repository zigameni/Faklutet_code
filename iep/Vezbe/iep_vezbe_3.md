# ORM (Object Relational Mapper) Notes

## SQLAlchemy Notes

### Overview

- The main purpose of ORM is to represent each table in a database as a class.
- There are specific rules for writing these classes to map relationships between primary and foreign keys.

### Relationships

1. **One-to-Many**: Represents the relationship between a primary and a foreign key.
2. **Many-to-Many**: Uses a linking table between two entities.

### Code Example: One-to-Many

```python
class Employee:  # Maps to table Employees
    __tablename__ = "employees"
    bonuses = db.relationship(
        "Bonus",
        backref="employee",
        lazy=True  # Fetches data as needed
    )

class Bonus:  # Maps to table Bonuses
    __tablename__ = "bonuses"
    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employee.id"),
        nullable=False
    )
```

### Code Example: Many-to-Many

```python
with application.app_context():
    database.create_all()
    # This creates the database based on the entity classes derived from the Model class
```

### Initialization

- Initialize the SQLAlchemy object within the application.
- Provide configuration via the config object.
- Example:

```python
db = SQLAlchemy(application)
```

### Example: Query with Group By

```python
query = database.session.query(
    Employee.id, func.count("*")
).join(
    Employee.tasks
).group_by(
    Employee.id
)
```

### Full Example: Using Models and Queries

```python
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    gender = db.Column(db.String(256), nullable=False)
    language = db.Column(db.String(256), nullable=False)
    position = db.Column(db.String(256), nullable=False)
    tasks = db.relationship("Task", back_populates="employee")

    def __init__(self, first_name, last_name, email, gender, language, position):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.language = language
        self.position = position

    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name}>"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    employee = db.relationship("Employee", back_populates="tasks")

with app.app_context():
    db.create_all()

@app.route('/bonuses', methods=['GET'])
def get_bonuses():
    query = Bonus.query
    reasons = request.args.getlist("reasons")
    # Example URL: http://localhost:5000/bonuses?reasons=PERFORMANCE&reasons=LOYALTY
    if reasons:
        query = query.filter(Bonus.reason.in_(reasons))
    bonuses = query.all()
    return jsonify([bonus.to_dict() for bonus in bonuses])
```

### Authentication and Authorization

1. **Authentication**: Verifying if a user is registered.
2. **Authorization**: Checking if a user has the right privileges.

### Tokens

- JSON Web Tokens (JWT) are used for stateless authentication.
- A JWT consists of three parts: header, payload, and signature.
- Example of standard fields:

- `iat`: Issued at timestamp
- `sub`: Subject (user identifier)
- `exp`: Expiry time
- `nbf`: Not valid before timestamp

### JWT Example in Flask

```python
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this in production
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # Validate user credentials here
    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

if __name__ == '__main__':
    app.run()
```

### Configuration Class

```python
class Configuration:
    JWT_SECRET_KEY = "your_secret_key"
    JWT_ACCESS_TOKEN_EXPIRES = 900  # 15 minutes
```

### Register and Login Methods

- **Registration**: Adds users to the database with appropriate privileges.
- **Login**: Verifies credentials and issues a token.

### Example for Configuration

```python
class Configuration:
    JWT_SECRET_KEY = "your_secret_key"
    JWT_ACCESS_TOKEN_EXPIRES = 900  # Tokens expire in 15 minutes
```

### Endpoint Example

```python
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    # Add user to the database
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"})
```

### Summary

- **SQLAlchemy**: Provides ORM capabilities.
- **Relationships**: Handles one-to-many and many-to-many relationships.
- **Initialization**: Configure and create the database using SQLAlchemy.
- **Queries**: Perform complex queries, including group by.
- **Authentication**: Using JWT for stateless authentication.
- **Configuration**: Securely configure your Flask application.

These notes should provide a structured overview of using SQLAlchemy and JWT for database and authentication management in Flask.
