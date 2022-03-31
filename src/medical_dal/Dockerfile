FROM python:3.10-alpine AS dev
WORKDIR /opt

COPY common /opt/common
RUN python -m pip install -e /opt/common

COPY medical_dal /opt/medical_dal
RUN python -m pip install -e /opt/medical_dal

ENV DEBUG=1

CMD python -m tmr