FROM python:3.10-alpine AS dev
WORKDIR /opt

RUN apk add build-base openldap-dev
RUN echo -n "INPUT ( libldap.so )" > /usr/lib/libldap_r.so

COPY common/requirements.txt /opt/common/requirements.txt
COPY common/setup.py /opt/common/setup.py
COPY common/tmr_common/__init__.py /opt/common/tmr_common/__init__.py
RUN python -m pip install -e /opt/common

COPY backend/requirements.txt /opt/backend/requirements.txt
COPY backend/setup.py /opt/backend/setup.py
COPY backend/tmr/__init__.py /opt/backend/tmr/__init__.py
RUN python -m pip install -e /opt/backend

ENV DEBUG=1
CMD python -m tmr

FROM python:3.10-alpine
WORKDIR /opt

RUN apk add build-base openldap-dev
RUN echo -n "INPUT ( libldap.so )" > /usr/lib/libldap_r.so

COPY common/requirements.txt /opt/common/requirements.txt
COPY common/setup.py /opt/common/setup.py
COPY common/tmr_common/__init__.py /opt/common/tmr_common/__init__.py
RUN python -m pip install -e /opt/common

COPY backend/requirements.txt /opt/backend/requirements.txt
COPY backend/setup.py /opt/backend/setup.py
COPY backend/tmr/__init__.py /opt/backend/tmr/__init__.py
RUN python -m pip install -e /opt/backend

COPY common /opt/common
COPY backend /opt/backend

CMD uvicorn tmr.app:app --host 0.0.0.0 --port 80