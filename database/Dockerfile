FROM mcr.microsoft.com/mssql/server:2019-latest

COPY init-db.sql /tmp/init-db.sql
COPY start.sh /tmp/start.sh

CMD ["/tmp/start.sh"]
