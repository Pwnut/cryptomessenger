FROM ubuntu:22.04
RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt install python3 python3-venv -y

ENV VENV=/opt/venv
RUN python3 -m venv $VENV

ENV PATH="$VENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir /app
COPY rsa_example.py /app

WORKDIR /app
CMD ["python3", "rsa_example.py"]
