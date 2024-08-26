FROM python:3.9.19-bullseye
WORKDIR /app
RUN pip install pika
COPY generator.py ./
CMD [ "python3", "generator.py" ]
