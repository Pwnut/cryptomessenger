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
COPY messenger.py /app
COPY database_interaction.py /app
COPY db_interaction.py /app
COPY client.py /app
COPY server.py /app
COPY messaging.proto /app
COPY encryption.py /app

#compile proto
RUN curl -LO https://github.com/protocolbuffers/protobuf/releases/download/v25.1/protoc-25.1-linux-x86_64.zip
RUN apt install unzip -y
RUN mkdir /app/.local
RUN unzip protoc-25.1-linux-x86_64.zip -d /app/.local
ENV PATH="$PATH:/app/.local/bin"
WORKDIR /app
RUN mkdir proto/
RUN protoc --python_out=proto/ messaging.proto
#CMD ["python3", "rsa_example.py"]
