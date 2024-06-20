FROM python:3

COPY ./configuration.py ./configuration.py
COPY ./models.py ./models.py
COPY ./main.py ./main.py
COPY ./requirements.txt ./requirements.txt

ENTRYPOINT [ "python", "main.py" ]