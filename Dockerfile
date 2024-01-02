FROM python:3.9-slim AS base

# Install dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends \ 
    build-essential \
    curl \
    software-properties-common \
    python3-dev \
    git \
    libatlas-base-dev \
    libopenblas-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv venv

# install the requirements into a build, to avoid reinstallation
FROM base as build-venv
RUN /venv/bin/pip3 install adafruit-circuitpython-shtc3  --no-cache-dir 
RUN /venv/bin/pip3 install plotly  --no-cache-dir
RUN /venv/bin/pip3 install streamlit  --no-cache-dir
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip3 install -r requirements.txt  --no-cache-dir

# Copy files into the build image
FROM build-venv as build
COPY . /app
WORKDIR /app

# Expose the default Flask port
EXPOSE 8080

HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

# Set the entrypoint to start the Flask app
ENTRYPOINT ["/venv/bin/python3", "-m", "streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]