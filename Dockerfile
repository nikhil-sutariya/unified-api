FROM python:3.10.12

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

EXPOSE 8080

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8080"]
