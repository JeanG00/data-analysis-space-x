FROM registry.cn-shanghai.aliyuncs.com/slatepencil/python:3.11-slim

# Keeps Python from generating .pyc files in the container.
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
# 
ENV FLASK_RUN_PORT=80


# Install pip requirements.
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

EXPOSE 80

COPY . /root/app
WORKDIR /root/app

# Creates a non-root user with an explicit UID and adds permission to access the /root/app folder.
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /root/app
# USER appuser

# Provides defaults for an executing container; can be overridden with Docker CLI.
CMD exec gunicorn -k gevent --bind 0.0.0.0:$FLASK_RUN_PORT -w 1 app:app