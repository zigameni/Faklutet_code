# Docker Setup and Configuration Guide

<div align="justify">

## Installation

1. Install Docker Desktop.

## Project Setup

1. Open a new Python project.
2. Create a `development.yaml` file which represents the configuration for Docker Compose. Docker Compose allows defining and running multiple containers in a Docker environment.

### Example `development.yaml` Configuration

```yaml
version: '3'  # Defines the version of Docker Compose

services:
  database:
    image: mysql  # Docker image to use for the container
    environment:
      - MYSQL_ROOT_PASSWORD=root  # MySQL root password
    ports:
      - 3305:3306  # Mapping host port 3305 to container port 3306

  adminer:
    image: adminer
    ports:
      - 8080:8080  # Mapping host port 8080 to container port 8080
```

## Docker Hub

- Docker Hub is a website where you can find libraries of images that can be used.
- Environment variable names for a given image can also be found there.

## Accessing Adminer

- Defining port 8080 allows access to Adminer via `http://localhost:8080`.
- Adminer is a database management tool that serves as a frontend for the database created in the MySQL container. It helps verify if services are running correctly.
- When both MySQL and Adminer services are started in the same `.yaml` file, Adminer directly accesses the database since they are automatically connected on the same network. If they are in different files, a specific network must be defined.

## Port Configuration

- **Host Port**: The port on the host operating system used for communication with the service inside the Docker container. This can be any free port on your system.
- **Container Port**: The port inside the Docker container. The service listens on this port for incoming connections.
- If port 3306 is already in use (likely due to a running MySQL server), change the host port to 3305 or any other free port.

### Important

- `host port:container port`
- For example, if `3306:3306` does not work, change it to `3305:3306`.

## Running the Configuration

1. Edit configuration.
2. Click on `+` and select Docker Compose.
3. Choose the path to the configuration file (`development.yaml`) and name the configuration (the name does not need to match the file name).
4. In the Services section, connect to Docker. Ensure Docker Desktop is running in the background for the connection.

### Using Adminer

- Access Adminer via `http://localhost:8080`.
- Use the service name for the database (defined in `development.yaml`) as the server name.
- Password is `root` as specified in the `development.yaml`.

### Database Operations in Adminer

- Create a new database with "Create database".
- Create a table with "Create table".
- Add data to the table with "New item".
- Note: Databases created via Adminer are erased when Docker containers are restarted.

## Using pymysql Library (Not required for the lab)

1. Install pymysql.
2. Connect to the database created via Adminer:

   ```python
   connection = pymysql.connect(
       host="localhost",
       port=3305,
       user="root",
       password="root",
       database="forum",
       cursorclass=pymysql.cursors.DictCursor
   )
   ```

### Database Operations

```python
with connection:
    with connection.cursor() as cursor:
        query = "SELECT * FROM threads"
        cursor.execute(query)
        print(cursor.fetchall())
```

## Creating Docker Image Files

### Example `Dockerfile`

```dockerfile
FROM ubuntu
ENTRYPOINT ["sleep", "1200"]
```

- `FROM ubuntu`: Specifies the base image.
- `ENTRYPOINT`: Command to run when the container starts.

### Example Project `Dockerfile`

```dockerfile
FROM python:3
COPY configuration.py /configuration.py
COPY models.py /models.py
COPY main.py /main.py
COPY requirements.txt /requirements.txt
RUN pip install -r ./requirements.txt
ENTRYPOINT ["python", "main.py"]

```

- This file copies the project files into the container and installs the required libraries before running `main.py`.

## Building an Image

1. Open Windows PowerShell.
2. Change the directory to the one containing the `Dockerfile`.
3. Execute the build command:

   ```sh

   docker build -f ./Dockerfile --tag myproject .

   ```

- `--tag myproject`: Names the image `myproject`.

## Using the Image in `development.yaml`

```yaml
services:
  myproject:
    image: myproject
    ports:
      - 5002:5002
    environment:
      - PRODUCTION="PRODUCTION"
```

- Add the service to `development.yaml`.

## Steps for Creating and Using Docker Images

1. Start Docker Desktop to launch the Docker engine.
2. Connect to the database:
   - If using a Flask app with MySQL, start the MySQL service via `development.yaml`.
   - Without this, you cannot connect to the database unless using Workbench (not recommended here).

### Example `configuration.py`

```python
import os

DATABASE_URL = "database" if "PRODUCTION" in os.environ else "localhost"
PORT = "3306" if "PRODUCTION" in os.environ else "3305"

class Configuration:
    SQLALCHEMY_DATABASE_URI = f"mysql://root:root@{DATABASE_URL}:{PORT}/employees"
```

- The syntax is: `mysql://username:password@url:port/database_name`.

### Initializing the Database

- Create an `init` folder in the project with an SQL script to initialize the database.
- Map this folder to `docker-entrypoint-initdb.d` in the MySQL image, which automatically executes scripts on MySQL server startup:
  
  ```yaml

  services:
    database:
      image: mysql
      environment:
        - MYSQL_ROOT_PASSWORD=root
      ports:
        - 3305:3306
      volumes:
        - ./init:/docker-entrypoint-initdb.d
  ```

  - In `init.sql`: `CREATE DATABASE employees;`

### Example `main.py`

```python
if __name__ == "__main__":
    databaseMade = False
    while not databaseMade:
        try:
            with application.app_context():
                database.create_all()
                databaseMade = True
        except Exception:
            pass

    HOST = "0.0.0.0" if "PRODUCTION" in os.environ else "127.0.0.1"
    application.run(debug=True, host=HOST)
```

- Ensure `database.create_all()` is within a loop to handle cases where the application starts before the MySQL server.
- Use `0.0.0.0` to make the application accessible outside the container.

## Final Steps

1. Write routes and queries for the Flask application.
2. Create a Dockerfile for the application.
3. Build the image and add it to `development.yaml`.
4. Start services and access the application via browser.

### Handling Multiple Components

- If you need multiple components running on different ports:
  
  ```python
  application.run(debug=True, host=HOST, port=5002)
  ```

- Ensure different ports are used for different components.

This comprehensive guide covers the essential steps and configurations needed to set up Docker for a Python project, including setting up MySQL and Adminer services, handling environment variables, and creating Docker images.

</div>
