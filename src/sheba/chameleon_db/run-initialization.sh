sleep 90s
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P Password123 -d master -i chameleon_db_script.sql
