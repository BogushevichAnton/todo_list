FROM python:3.12.6
#set env logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY req.txt ./
RUN apt-get update && apt-get install -y --no-install-recommends bash && pip install --no-cache-dir -r req.txt

COPY . .
RUN chmod +x /usr/src/app/django.sh
ENTRYPOINT ["/bin/bash", "/usr/src/app/django.sh"]