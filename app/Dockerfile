FROM ubuntu:22.04

ENV ubuntu_version=22.04
ENV ACCEPT_EULA=Y

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt install python3 python3-venv nano unixodbc curl iputils-ping -y
RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc
RUN curl https://packages.microsoft.com/config/ubuntu/$ubuntu_version/prod.list | tee /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update -y
RUN apt-get install -y msodbcsql18
RUN apt-get install -y mssql-tools18
ENV PATH="$PATH:/opt/mssql-tools18/bin"

ENV VENV=/opt/venv
RUN python3 -m venv $VENV

ENV PATH="$VENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir /app
COPY pub_key_trade_poc.py /app
COPY database_interaction.py /app
COPY db_interaction.py /app

WORKDIR /app
#CMD ["python3", "rsa_example.py"]
