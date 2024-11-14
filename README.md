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

Happy coding!
