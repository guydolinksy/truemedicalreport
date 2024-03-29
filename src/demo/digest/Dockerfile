FROM python:3.10.8-alpine3.15 AS dev
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


ENV DEBUG=1
CMD python -m digest

FROM python:3.10.8-alpine3.15
ENV HOME=/opt
WORKDIR /opt

RUN apk add build-base unixodbc unixodbc-dev
RUN apk add curl
RUN curl -O https://download.microsoft.com/download/b/9/f/b9f3cce4-3925-46d4-9f46-da08869c6486/msodbcsql18_18.0.1.1-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/b/9/f/b9f3cce4-3925-46d4-9f46-da08869c6486/mssql-tools18_18.0.1.1-1_amd64.apk

RUN apk add --allow-untrusted msodbcsql18_18.0.1.1-1_amd64.apk
RUN apk add --allow-untrusted mssql-tools18_18.0.1.1-1_amd64.apk

COPY common/requirements.txt /opt/common/requirements.txt
COPY common/setup.py /opt/common/setup.py
COPY common/common/__init__.py /opt/common/common/__init__.py
RUN python -m pip install -e /opt/common

COPY demo/digest/requirements.txt /opt/digest/requirements.txt
COPY demo/digest/setup.py /opt/digest/setup.py
COPY demo/digest/digest/__init__.py /opt/digest/digest/__init__.py
RUN python -m pip install -e /opt/digest

COPY common/common /opt/common/common
COPY demo/digest/digest /opt/digest/digest

CMD uvicorn digest.app:app --host 0.0.0.0 --port 80
