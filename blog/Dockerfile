FROM python:3
WORKDIR /usr/src/app
COPY ./requirements.py .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]