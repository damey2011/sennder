FROM python:3.8.2-alpine
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . /code
EXPOSE 80