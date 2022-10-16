FROM python:3.10-alpine AS dev
WORKDIR /opt

RUN apk add build-base openldap-dev
RUN echo -n "INPUT ( libldap.so )" > /usr/lib/libldap_r.so

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

FROM python:3.10-alpine
WORKDIR /opt

RUN apk add build-base openldap-dev
RUN echo -n "INPUT ( libldap.so )" > /usr/lib/libldap_r.so

COPY common/requirements.txt /opt/common/requirements.txt
COPY common/setup.py /opt/common/setup.py
COPY common/common/__init__.py /opt/common/common/__init__.py
RUN python -m pip install -e /opt/common

COPY dal/requirements.txt /opt/dal/requirements.txt
COPY dal/setup.py /opt/dal/setup.py
COPY dal/dal/__init__.py /opt/dal/dal/__init__.py
RUN python -m pip install -e /opt/dal

COPY common/common /opt/common/common
COPY dal/dal /opt/dal/dal

CMD uvicorn dal.app:app --host 0.0.0.0 --port 80
