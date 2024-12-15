FROM python:3.12.6

#set env logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /todo_drf

COPY req.txt /todo_drf/
RUN pip install -r req.txt

COPY . /todo_drf/
COPY django.sh .
RUN chmod +x ./django.sh

ENTRYPOINT ["/bin/sh", "./django.sh"]
