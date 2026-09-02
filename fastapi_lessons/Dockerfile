FROM python:3.12.10

WORKDIR /app


COPY lesson1.py ./Dockerfile ./requirements.txt ./
#COPY . .

RUN pip install -r requirements.txt



CMD ["python", "main.py"]
