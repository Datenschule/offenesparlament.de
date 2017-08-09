FROM python:3.6.1-alpine

ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "-w 4", "--bind=0.0.0.0:8000", "app:app"]