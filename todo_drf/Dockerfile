FROM python:3.12.6
#set env logs

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY ./req.txt .
RUN pip install -r req.txt
COPY ./django.sh .
COPY . .
RUN chmod +x ./django.sh
ENTRYPOINT ["/bin/sh", "./django.sh"]