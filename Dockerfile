FROM python:2.7.13-alpine

WORKDIR /app

ADD . /app

RUN pip install -r pip-freeze.txt

CMD ["python","/app/runserver.py"]
