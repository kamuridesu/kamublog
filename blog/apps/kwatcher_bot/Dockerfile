FROM python:3.11-rc-slim-bullseye
RUN pip3 install python-telegram-bot==13.10
RUN pip3 install Flask==2.0.1
COPY . .
CMD ["python", "routes.py"]