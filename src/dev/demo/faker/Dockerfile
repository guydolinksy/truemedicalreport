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
COPY common/common/__init__.py /opt/common/common/

RUN python -m pip install -e /opt/common

COPY demo/digest/setup.py /opt/digest/
COPY demo/digest/requirements.txt /opt/digest/
COPY demo/digest/digest/__init__.py /opt/digest/digest/
RUN python -m pip install -e /opt/digest

COPY dev/demo/faker/setup.py /opt/faker/
COPY dev/demo/faker/requirements.txt /opt/faker/
COPY dev/demo/faker/tmr_faker/__init__.py /opt/faker/tmr_faker/
RUN python -m pip install -e /opt/faker


COPY common /opt/common
COPY demo/digest/digest /opt/digest/digest
COPY dev/demo/faker/tmr_faker /opt/faker/tmr_faker

ENV DEBUG=1

CMD python -m tmr_faker