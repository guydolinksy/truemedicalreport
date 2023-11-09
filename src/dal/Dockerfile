FROM python:3.10.8-alpine3.15 AS dev
WORKDIR /opt

RUN apk add build-base openldap-dev
RUN echo -n "INPUT ( libldap.so )" > /usr/lib/libldap_r.so

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

COPY dal/requirements.txt /opt/dal/requirements.txt
COPY dal/setup.py /opt/dal/setup.py
COPY dal/dal/__init__.py /opt/dal/dal/__init__.py
RUN python -m pip install -e /opt/dal

ENV DEBUG=1
CMD python -m dal


FROM guydo/tmr-dal:dev AS prod

COPY common/common /opt/common/common
COPY dal/dal /opt/dal/dal

CMD uvicorn dal.app:app --host 0.0.0.0 --port 80
