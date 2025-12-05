FROM python:3.13.7-slim

# NOTE: for alpine use this line
# RUN apk add --no-cache bash

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src 
COPY entry.sh .

ENV PYTHONPATH=/app/src

RUN chmod +x entry.sh

EXPOSE 8080

ENTRYPOINT ["./entry.sh"]
