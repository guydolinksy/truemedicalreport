TIMEOUT=90
for i in $(seq 1 $TIMEOUT);
  do
    /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $SA_PASSWORD -d master -i /opt/arc_db/initialize/arc_db.sql
    if [ $? -eq 0 ]
    then
        break
    else
        sleep 5
    fi
done