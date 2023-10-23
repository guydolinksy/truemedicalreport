##newer version install openssl 3 which pypdbc connections to mssql
#FROM python:3.10.8-alpine3.15 AS dev
#ENV HOME=/opt
#
#RUN apk add build-base unixodbc unixodbc-dev
#RUN apk add curl
#RUN curl -O https://download.microsoft.com/download/b/9/f/b9f3cce4-3925-46d4-9f46-da08869c6486/msodbcsql18_18.0.1.1-1_amd64.apk
#RUN curl -O https://download.microsoft.com/download/b/9/f/b9f3cce4-3925-46d4-9f46-da08869c6486/mssql-tools18_18.0.1.1-1_amd64.apk
#
#RUN apk add --allow-untrusted msodbcsql18_18.0.1.1-1_amd64.apk
#RUN apk add --allow-untrusted mssql-tools18_18.0.1.1-1_amd64.apk
#
#COPY common/setup.py /opt/common/
#COPY common/requirements.txt /opt/common/
#COPY common/common/__init__.py /opt/common/common/
#
#RUN python -m pip install -e /opt/common
#
#COPY sheba/digest/setup.py /opt/digest/
#COPY sheba/digest/requirements.txt /opt/digest/
#COPY sheba/digest/digest/__init__.py /opt/digest/digest/
#
#RUN python -m pip install -e /opt/digest
#
#
#ENV DEBUG=1
#CMD python -m digest

FROM guydo/tmr-sheba-digest:dev AS prod

COPY common/common /opt/common/common
COPY sheba/digest/digest /opt/digest/digest

CMD uvicorn digest.app:app --host 0.0.0.0 --port 80
