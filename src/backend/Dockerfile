#FROM python:3.10.8-alpine3.15 AS dev
#WORKDIR /opt
#
#RUN apk add build-base openldap-dev
#RUN echo -n "INPUT ( libldap.so )" > /usr/lib/libldap_r.so
#
#COPY common/requirements.txt /opt/common/requirements.txt
#COPY common/setup.py /opt/common/setup.py
#COPY common/common/__init__.py /opt/common/common/__init__.py
#RUN python -m pip install -e /opt/common
#
#COPY backend/requirements.txt /opt/backend/requirements.txt
#COPY backend/requirements-ldap.txt /opt/backend/requirements-ldap.txt
#COPY backend/setup.py /opt/backend/setup.py
#COPY backend/backend/__init__.py /opt/backend/backend/__init__.py
#RUN python -m pip install -e /opt/backend[ldap]
#
#ENV DEBUG=1
#CMD python -m backend

FROM guydo/tmr-backend:dev AS prod

COPY common/common /opt/common/common
COPY backend/backend /opt/backend/backend

CMD uvicorn backend.app:app --host 0.0.0.0 --port 80
