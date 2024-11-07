FROM mcr.microsoft.com/mssql/server:2019-latest

ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=WeHacking808

COPY init-db.sql /init-db.sql

CMD /opt/mssql/bin/sqlservr & sleep 15 && /opt/mssql-tools18/bin/sqlcmd -S localhost -U SA -P $SA_PASSWORD -i /init-db.sql -C
