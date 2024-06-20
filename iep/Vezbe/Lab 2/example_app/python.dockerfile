# Linux os with python
FROM python:3

# copy source code and dependency list 
COPY ./configuration.py ./configuration.py
COPY ./requirements.txt ./requirements.txt
COPY ./models.py ./models.py
COPY ./main.py ./main.py

# install dependencies
RUN pip install -r requirements.txt

# start container 
ENTRYPOINT [ "python", "main.py" ]