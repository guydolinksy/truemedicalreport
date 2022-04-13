FROM python:3.10-alpine AS dev
WORKDIR /opt

RUN apk add build-base openldap-dev
RUN echo -n "INPUT ( libldap.so )" > /usr/lib/libldap_r.so

COPY common /opt/common
RUN python -m pip install -e /opt/common


COPY backend /opt/backend
RUN python -m pip install -e /opt/backend

ENV DEBUG=1

CMD python -m tmr