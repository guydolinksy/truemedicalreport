FROM mcr.microsoft.com/mssql/server:2019-latest
WORKDIR /opt
ENV ACCEPT_EULA=Y

COPY dev/sheba/chameleon/entrypoint.sh /opt/chameleon/entrypoint.sh
COPY dev/sheba/chameleon/initialize /opt/chameleon/initialize

CMD sh /opt/chameleon/entrypoint.sh
