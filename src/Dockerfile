FROM python:3.10-alpine AS dev

RUN apk add build-base openldap-dev unixodbc-dev
RUN echo -n "INPUT ( libldap.so )" > /usr/lib/libldap_r.so
COPY common/requirements.txt /opt/dev/requirements.common.txt
RUN python -m pip install -r /opt/dev/requirements.common.txt
COPY dal/requirements.txt /opt/dev/requirements.dal.txt
RUN python -m pip install -r /opt/dev/requirements.dal.txt
COPY backend/requirements.txt /opt/dev/requirements.backend.txt
RUN python -m pip install -r /opt/dev/requirements.backend.txt
COPY backend/requirements-ldap.txt /opt/dev/requirements-ldap.backend.txt
RUN python -m pip install -r /opt/dev/requirements-ldap.backend.txt
COPY sheba/digest/requirements.txt /opt/dev/requirements.digest.txt
RUN python -m pip install -r /opt/dev/requirements.digest.txt

CMD ["tail", "-f", "/dev/null"]
