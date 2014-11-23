FROM python:2.7.8

RUN pip install Requests Flask flask-triangle tornado

COPY src/ /src/

EXPOSE 80

CMD python /src/tornado-webserver.py