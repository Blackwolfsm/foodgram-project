FROM python:3.8.5

WORKDIR /code
COPY . ./
RUN pip install -r /code/requirements.txt
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=ru_RU.UTF-8
ENV LANG ru_RU.UTF-8 
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8005