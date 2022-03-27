FROM python:3.9-alpine AS dev
ENV HOME=/opt/
COPY bootstrap /opt/bootstrap
RUN python /opt/bootstrap/setup.py develop

CMD python -m bootstrap $ENVIRONMENT