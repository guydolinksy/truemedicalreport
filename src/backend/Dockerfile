FROM python:3.10-alpine AS dev
WORKDIR /opt
COPY . /opt/backend
RUN pip install --no-cache-dir --upgrade -r /opt/backend/requirements.txt
RUN python -m backend.tmr