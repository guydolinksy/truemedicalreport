FROM mcr.microsoft.com/mssql/server:2019-latest
WORKDIR /opt
ENV ACCEPT_EULA=Y

COPY dev/sheba/arc-db/entrypoint.sh /opt/arc-db/entrypoint.sh
COPY dev/sheba/arc-db/initialize /opt/arc-db/initialize

CMD sh /opt/arc-db/entrypoint.sh
