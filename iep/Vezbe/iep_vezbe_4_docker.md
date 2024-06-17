# Docker Notes

## Overview

We have network servers running virtual machines, which are flexible but take up around 40GB each. Instead, we use orchestrators, with Docker being one of them.

Docker is a virtualization tool that virtualizes the OS, providing programs with the illusion of an operating system. Unlike standard virtualizers (e.g., VMware) that virtualize hardware and run a full OS on top of it, Docker virtualizes the OS itself, making it lightweight and efficient.

## Docker Basics

### Installation

We use the community version of Docker, which is installed in our lab. Before installation, ensure no active hypervisor (such as Hyper-V on Intel machines) is running, as it may need to be disabled.

### Running Containers

To create a container, we need an image, which acts as a template. Images can be custom-made from our application or downloaded from the Docker Hub repository.

#### Example Commands

```sh
# Run a container from the hello-world image
docker run hello-world
```

- The command above runs a container based on the `hello-world` image from the Docker repository.
- It doesn't matter from which path you run the command, as all executables should be in the PATH variables.

There is a public repository, Docker Hub, where you can find containers for many tools used during studies, such as PHP interpreters, MySQL databases, etc.

```sh
# Run a hello-world container
docker run hello-world
```

- This command will fetch the image from the global repository if it is not available locally and then run it.

```sh
# Run an Ubuntu container with an interactive terminal
docker run -it ubuntu bash
```

- This command runs the Ubuntu operating system in a container.
- We can see the list of running images and manage them using Docker commands.
- Docker assigns a name to each container, and we can see the image from which a container was created.

### Working with Containers

We will use the Ubuntu OS, copy our files into the container, and run them. We can use the console to make changes as needed. Each container is assigned an entry point and remains alive as long as the command specified at the entry point is running (e.g., `bash`). The container will stop when the entry point command is closed.

With the `compose` command, all outputs are displayed unless specified otherwise, whereas with the `run` command, the outputs are not displayed by default.

### Using MySQL with Docker

```sh
# Run a MySQL container
docker run mysql
```

- Refer to the Docker Hub MySQL page for all details about the image. When running the image, you can specify which version to use.
- Docker containers are parameterized by specifying a set of environment variables for each container.

```sh
# Example of specifying a MySQL root password
docker run -e MYSQL_ROOT_PASSWORD=my-secret-pw mysql
```

- The command above sets the root password for the MySQL container.

To connect to the MySQL database, you can use any client application, such as MySQL Workbench.

Our server runs locally, and all requests are sent through a specified port. If not specified, the default MySQL port 3306 is used.

#### Exposing Ports

When working with containers, there is a concept of Docker Host - the physical machine running Docker. All containers within the host act like virtual machines. While containers within the host can communicate without issues, accessing containers externally requires port specification.

```sh
# Expose ports when running a MySQL container
docker run -p 6603:3306 mysql
```

- The command maps the physical port 6603 to the virtual port 3306 used by the MySQL container.
- Now, all requests to port 6603 will be forwarded to the MySQL container.

### Handling Multiple Containers

If we have two containers with the same name, we must use the `--name` option to assign unique names to each container.

### Configuring Applications to Use MySQL

To configure our application to use the MySQL database, we need to change the database connection string.

```python
# Example connection string for SQLAlchemy
SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost:6603/users"
```

- The connection string format is `database://username:password@host:port/database_name`.
- If the port is not specified, the default MySQL port 3306 is assumed. Since we use port 6603, it must be included in the connection string.

Using `pymysql` as a driver, the connection string would be:

```python
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:6603/users"
```

## Summary

Docker provides a lightweight and efficient way to virtualize applications by virtualizing the OS rather than the hardware. It is straightforward to use, and with Docker Hub, you can easily find and run containers for various applications and services. Properly exposing ports and configuring connection strings allows seamless integration with applications such as MySQL databases.
