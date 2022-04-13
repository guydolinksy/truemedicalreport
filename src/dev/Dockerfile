FROM python:3.10-alpine AS dev

RUN apk add build-base openldap-dev unixodbc-dev
RUN echo -n "INPUT ( libldap.so )" > /usr/lib/libldap_r.so
COPY common/requirements.txt /opt/dev/requirements.common.txt
RUN python -m pip install -r /opt/dev/requirements.common.txt
COPY medical_dal/requirements.txt /opt/dev/requirements.medical_dal.txt
RUN python -m pip install -r /opt/dev/requirements.medical_dal.txt
COPY backend/requirements.txt /opt/dev/requirements.backend.txt
RUN python -m pip install -r /opt/dev/requirements.backend.txt
COPY sheba/ingress/requirements.txt /opt/dev/requirements.ingress.txt
RUN python -m pip install -r /opt/dev/requirements.ingress.txt
