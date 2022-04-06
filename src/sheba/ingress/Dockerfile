FROM python:3.10-alpine AS dev
ENV HOME=/opt

RUN apk add build-base unixodbc unixodbc-dev

COPY common/setup.py /opt/common/
COPY common/requirements.txt /opt/common/
COPY common/tmr_common/__init__.py /opt/common/tmr_common/

RUN python -m pip install -e /opt/common

COPY sheba/ingress/setup.py /opt/ingress/
COPY sheba/ingress/requirements.txt /opt/ingress/
COPY sheba/ingress/tmr_ingress/__init__.py /opt/ingress/tmr_ingress/
RUN python -m pip install -e /opt/ingress

COPY sheba/ingress/tmr_ingress /opt/ingress/tmr_ingress

COPY common /opt/common

CMD python -m tmr_ingress