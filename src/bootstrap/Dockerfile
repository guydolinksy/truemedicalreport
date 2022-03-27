FROM python:3.9-alpine AS dev
ENV HOME=/opt
COPY bootstrap /opt/bootstrap
RUN python -m pip install -e /opt/bootstrap develop

#CMD sleep 1000
CMD python -m bootstrap $ENVIRONMENT