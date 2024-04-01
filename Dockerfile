FROM python:3.11.7-alpine3.19
WORKDIR /opt
COPY . /opt
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1
RUN pip install --no-cache-dir -r /opt/requirements.txt
