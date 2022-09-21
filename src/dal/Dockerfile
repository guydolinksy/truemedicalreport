FROM python:3.10-alpine AS dev
WORKDIR /opt

COPY common /opt/common
RUN python -m pip install -e /opt/common

COPY dal /opt/dal
RUN python -m pip install -e /opt/dal

ENV DEBUG=1

CMD python -m tmr