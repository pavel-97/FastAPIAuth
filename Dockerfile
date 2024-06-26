FROM python:3.12
EXPOSE 8001

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
COPY src ./src
RUN pip install -r requirements.txt
CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]