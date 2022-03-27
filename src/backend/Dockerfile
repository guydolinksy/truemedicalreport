FROM python:3.10-alpine AS dev
WORKDIR /opt

COPY backend /opt/backend
RUN python -m pip install -e /opt/backend

CMD python -m tmr