FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
CMD [ "python3", "src/stac_ingester/nats_consumer.py" ]
