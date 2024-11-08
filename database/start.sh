/opt/mssql/bin/sqlservr &
sleep 10
/opt/mssql-tools18/bin/sqlcmd -S localhost -U SA -P $SA_PASSWORD -i /tmp/init-db.sql -C
