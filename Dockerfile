FROM python:3.12-slim-buster

WORKDIR /todo_list

COPY requirements.txt .
RUN pip install --no-cache-dir -r req.txt

COPY . .

CMD ["python", "manage.py", "migrate"]