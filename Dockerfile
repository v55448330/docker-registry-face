FROM python:2.7.13-alpine

ENV REGISTRY_URL
ENV REGISTRY_USER
ENV REGISTRY_PASSWORD

WORKDIR /app

ADD . /app

RUN pip install -r pip-freeze.txt

CMD ["python","/app/runserver.py"]