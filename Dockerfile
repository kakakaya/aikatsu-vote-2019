FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN apt update && apt full-upgrade -y

COPY ./requirements.txt /app
RUN pip install -r requirements.txt
