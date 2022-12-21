FROM mcr.microsoft.com/mssql/server:2019-latest as dev
WORKDIR /opt
ENV ACCEPT_EULA=Y

COPY dev/demo/demo-db/entrypoint.sh /opt/demo-db/entrypoint.sh
COPY dev/demo/demo-db/initialize /opt/demo-db/initialize

CMD sh /opt/demo-db/entrypoint.sh
