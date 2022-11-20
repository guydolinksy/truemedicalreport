INIT_MARKER_FILE=/var/opt/mssql/initialized

if [ -f "$INIT_MARKER_FILE" ]; then
  echo "This DB was already initialized."
  echo "If you want to re-initialize, drop the docker volume"
  exit 0
fi

TIMEOUT=90
for i in $(seq 1 $TIMEOUT);
  do
    /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -d master -i /opt/chameleon/initialize/init.sql
    if [ $? -eq 0 ]
    then
        touch "$INIT_MARKER_FILE"
        break
    else
        sleep 5
    fi
done
