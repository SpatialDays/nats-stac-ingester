FROM python:3.9-slim

COPY src /src

RUN pip install -e /src/
