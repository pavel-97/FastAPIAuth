FROM python:3.12
EXPOSE 8000

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
COPY ./src .
RUN pip install -r requirements.txt

CMD [ "uvicorn", "src/main:app"]