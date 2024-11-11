/opt/mssql/bin/sqlservr &
echo "Waiting for MySQL to be ready..."
until /opt/mssql-tools18/bin/sqlcmd -S localhost -U SA -P $SA_PASSWORD -i /tmp/init-db.sql -C; do
    echo "Waiting for MySQL..."
    sleep 2
done;
tail -F anything
