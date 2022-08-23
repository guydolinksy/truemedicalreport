FROM mcr.microsoft.com/mssql/server:2019-latest
WORKDIR /opt
ENV ACCEPT_EULA=Y

COPY sheba/arc_db/entrypoint.sh /opt/arc_db/entrypoint.sh
COPY sheba/arc_db/initialize /opt/arc_db/initialize

CMD sh /opt/arc_db/entrypoint.sh
