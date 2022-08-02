FROM python:3.9.5-slim-buster

LABEL maintainer "Juanse Vargas <juan.sebastian@loka.com>"

RUN apt-get update

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4000

CMD ["flask", "run", "--host=0.0.0.0", "--port=4000"]