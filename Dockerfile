FROM python:3.12-bookworm

WORKDIR /app

COPY ./app /app/app

COPY requirements.txt /app
RUN pip install setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
