FROM python:3.9.19-bullseye
WORKDIR /app
COPY proccesor.py ./
RUN pip install psycopg2 pika
CMD [ "python3", "proccesor.py" ]    