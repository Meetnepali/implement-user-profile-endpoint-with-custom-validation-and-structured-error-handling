FROM python:3.11-slim
WORKDIR /usr/src/app
COPY ./app ./app
RUN pip install --no-cache-dir fastapi==0.110.2 uvicorn==0.29.0
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
