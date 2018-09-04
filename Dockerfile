FROM python:3.6-alpine
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src .
CMD [ "gunicorn", "--bind", "0.0.0.0:80", "wsgi" ]
