FROM resin/rpi-raspbian:jessie
ADD https://github.com/jgarff/rpi_ws281x/archive/master.zip /
RUN apt-get update && \
    apt-get install -y build-essential \
        python-dev \
        scons \
        swig \
        unzip \
    --no-install-recommends && \
    rm -r /var/lib/apt/lists/* && \
    unzip master.zip && \
    cd rpi_ws281x-master && \
    scons && \
    cd python && \
    python ./setup.py install && \
    rm -rf ./build
COPY docker-leds.py /
CMD [ "python", "/docker-leds.py" ]

