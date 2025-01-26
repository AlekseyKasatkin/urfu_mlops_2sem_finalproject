# Dockerfile
FROM python:3.8-slim

WORKDIR /mlops_proj

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /mlops_proj/app/

RUN mkdir /mlops_proj/data

EXPOSE 8000

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
