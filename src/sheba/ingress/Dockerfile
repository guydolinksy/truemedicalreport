FROM python:3.10-alpine AS dev
ENV HOME=/opt

RUN apk add build-base unixodbc unixodbc-dev
RUN apk add curl
RUN curl -O https://download.microsoft.com/download/b/9/f/b9f3cce4-3925-46d4-9f46-da08869c6486/msodbcsql18_18.0.1.1-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/b/9/f/b9f3cce4-3925-46d4-9f46-da08869c6486/mssql-tools18_18.0.1.1-1_amd64.apk

RUN apk add --allow-untrusted msodbcsql18_18.0.1.1-1_amd64.apk
RUN apk add --allow-untrusted mssql-tools18_18.0.1.1-1_amd64.apk

COPY common/setup.py /opt/common/
COPY common/requirements.txt /opt/common/
COPY common/tmr_common/__init__.py /opt/common/tmr_common/

RUN python -m pip install -e /opt/common

COPY sheba/ingress/setup.py /opt/ingress/
COPY sheba/ingress/requirements.txt /opt/ingress/
COPY sheba/ingress/tmr_ingress/__init__.py /opt/ingress/tmr_ingress/
RUN python -m pip install -e /opt/ingress


COPY common /opt/common

COPY sheba/ingress/tmr_ingress /opt/ingress/tmr_ingress

ENV DEBUG=1

CMD python -m tmr_ingress