FROM python:3.7

# Do install pulsar-client from pip
RUN pip install pulsar-client

# The working directory is the current
WORKDIR /pulsar-client

# Copy local files the the workdir
COPY . .

# Entrypoint is on bash
# ENTRYPOINT ["/bin/sh", "-c", "while sleep 1000; do :; done"]
