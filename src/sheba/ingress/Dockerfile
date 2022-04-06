FROM python:3.10-alpine AS dev
ENV HOME=/opt


COPY sheba/ingress/setup.py /opt/ingress/
COPY sheba/ingress/requirements.txt /opt/ingress/
COPY sheba/ingress/tmr_ingress/__init__.py /opt/ingress/tmr_ingress/
RUN python -m pip install -e /opt/ingress develop

COPY sheba/ingress/tmr_ingress /opt/ingress/tmr_ingress

CMD python -m tmr_ingress