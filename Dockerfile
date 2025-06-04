FROM python:3.12

RUN apt-get update && apt-get install -y cron

WORKDIR /app

COPY ./requirements.txt ./


RUN pip install -r requirements.txt

COPY . .

COPY ./crontab /etc/cron.d/crontab

RUN chmod 0644 /etc/cron.d/crontab && crontab /etc/cron.d/crontab

RUN touch /var/log/cron.log


CMD ["sh","-c","cron && python3 telegramBot.py "]