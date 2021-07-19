# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

RUN apt-get update \
    && apt-get install -y cron

EXPOSE 8501

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

#CMD ["cron", "-f"]

CMD streamlit run index.py & cron -f
