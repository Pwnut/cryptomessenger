FROM mcr.microsoft.com/mssql/server:2019-latest

ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=WeHacking808

COPY init-db.sql /tmp/init-db.sql
COPY start.sh /tmp/start.sh

CMD ["/tmp/start.sh"]
