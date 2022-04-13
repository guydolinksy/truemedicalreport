FROM mcr.microsoft.com/mssql/server:2019-latest
ENV SA_PASSWORD=Password123
ENV ACCEPT_EULA=Y
ENV MSSQL_TCP_PORT=1433

WORKDIR /opt/chameleon_db
COPY ./sheba/chameleon_db .


EXPOSE 1433


CMD sh /opt/chameleon_db/entrypoint.sh
