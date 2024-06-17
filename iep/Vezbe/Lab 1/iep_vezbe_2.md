# Flask and SQLAlchemy Notes

## Application Context

When performing any operations outside of request handling, it must be done in the application context.

## SQLAlchemy Overview

- SQLAlchemy infers table names from class names and column names from attribute names.
- To specify a different table name, use `__tablename__`.

```python
class Employee(database.Model):
    __tablename__ = 'new_table_name'
```

## Adding Data to the Database

- `database.session` is the current open session to the database, managed automatically by SQLAlchemy.

```python
new_employee = Employee(column1=value1, column2=value2, ...)
database.session.add(new_employee)
database.session.commit()
```

- The changes will not be committed to the database until `commit()` is called.

## Querying Data

- To get all employees from the `Employee` table:

```python
employees = Employee.query.all()
```

- This is a query object that can be further refined using filters or other query methods.

```python
print(employees)  # Prints the SQL query that will be executed
jsonify(employees=[str(employee) for employee in employees.all()])
```

- The `all()` method fetches all rows that match the query, while `first()` fetches the first result.

## Defining Models

- Models in SQLAlchemy are Python classes that map to database tables.

```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

database = SQLAlchemy()
migrate = Migrate()

class Employee(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    first_name = database.Column(database.String(256), nullable=False)
    last_name = database.Column(database.String(256), nullable=False)
    email = database.Column(database.String(256), nullable=False)
    gender = database.Column(database.String(256), nullable=False)
    language = database.Column(database.String(256), nullable=False)
    position = database.Column(database.String(256), nullable=False)
    tasks = database.relationship("Task", back_populates="employee")

    def __init__(self, first_name, last_name, email, gender, language, position):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.language = language
        self.position = position

    def __repr__(self):
        return f"<Employee {self.first_name}, {self.last_name}>"

class Task(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    description = database.Column(database.String(256), nullable=False)
    employee_id = database.Column(database.Integer, database.ForeignKey('employee.id'), nullable=False)
    employee = database.relationship("Employee", back_populates="tasks")
```

## Filtering Queries

- Filtering results with the `filter` method:

```python
result = Employee.query.filter(Employee.id == 5).all()
```

- Adding dynamic filters based on request arguments:

```python
criteria = ["first_name", "last_name", ...]
filters = []

for criterium in criteria:
    if criterium in request.args:
        filters.append(getattr(Employee, criterium).like(f"%{request.args[criterium]}%"))

result = Employee.query.filter(*filters).all()
```

- This dynamically builds a list of filters and applies them to the query.

## Aggregating Data

- Using SQL functions like `count` with SQLAlchemy:

```python
from sqlalchemy import func

result = database.session.query(
    Employee.gender, func.count("*")
).group_by(Employee.gender)
```

- To add a `HAVING` clause:

```python
result = database.session.query(
    Employee.gender, func.count("*")
).group_by(Employee.gender).having(func.count("*") > 20)
```

## JSON Responses

- Returning JSON from a query:

```python
jsonify(result=[data for data in query_result])
```

## Application Context for Database Initialization

- Creating the database within the application context:

```python
with application.app_context():
    database.create_all()
```

- This is used for initial database creation but not for migrations.

## Database Migrations

- Migrations are like version control for your database schema.

### Setting Up Migrations

```python
from flask_migrate import Migrate

migrate = Migrate(application, database)
```

- Initialize the migration repository:

```bash
flask db init --app main:application
```

- Create a migration script:

```bash
flask db migrate -m "message describing changes"
```

- Apply the migration to the database:

```bash
flask db upgrade
```

### Downgrading Migrations

- Revert to a previous migration:

```bash
flask db downgrade
```

### Checking Migration Versions

- Alembic (used by Flask-Migrate) adds a `alembic_version` table to track applied migrations.

## Summary

- Use SQLAlchemy to manage database operations with Python classes.
- Use Flask-Migrate to handle database schema changes.
- Always perform operations outside of request handling in the application context.
- Use query methods and filters to interact with your database in a secure and efficient manner.
