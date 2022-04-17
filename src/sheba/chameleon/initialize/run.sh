TIMEOUT=60
for i in $(seq 1 $TIMEOUT)
do
    /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $SA_PASSWORD -d master -i /opt/chameleon/initialize/chameleon.sql
    if [ $? -eq 0 ]
    then
        break
    else
        sleep 1
    fi
done