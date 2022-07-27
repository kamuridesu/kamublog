FROM python:3.11-rc-slim-bullseye
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"] 
