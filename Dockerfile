FROM python:3.9.10


WORKDIR /app

COPY requirements.txt ./
COPY script.py ./

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["python", "script.py"]
