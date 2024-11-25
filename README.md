# cryptomessenger
An RSA-based cryptomessenger for communication between machines via CLI

## Usage
First, build the containter:
```bash
docker build -t cryptomessenger .
```

Then you can run it with:
```bash
docker run cryptomessenger
```

But if you want a shell within the docker container instead, run:
```bash
docker run -it cryptomessenger /bin/bash
```
## Features
- User registration and management
- Message encryption and decryption
- CLI and GUI interfaces
- Database integration with SQL Server
- RSA-based key management

## Requirements
- Docker
- Python 3.10 or later
- SQL Server with ODBC Driver 18 for SQL Server

Happy coding!
