FROM python:3.8.9

# Update Ubuntu and install dependencies
RUN apt update \
    && apt-get install -y libssl-dev libpcre3 libpcre3-dev

# Install CMake
RUN wget https://github.com/Kitware/CMake/releases/download/v3.20.0/cmake-3.20.0.tar.gz \
    && tar -zxvf cmake-3.20.0.tar.gz \
    && cd cmake-3.20.0 \
    && ./bootstrap \
    && make \
    && make install 

# Install SWIG
RUN wget http://prdownloads.sourceforge.net/swig/swig-4.0.2.tar.gz \
    && tar -zxvf swig-4.0.2.tar.gz \
    && cd swig-4.0.2 \
    && ./configure \
    && make \
    && make install

# Copy over the directory and make it the primary directory
COPY . /market_making_arbitrage
WORKDIR /market_making_arbitrage

# Build CCAPI
RUN cd ccapi \
    && mkdir binding/build \
    && cd binding/build \
    && cmake -DCMAKE_PROJECT_INCLUDE=/market_making_arbitrage/user_specified_cmake_include.cmake -DBUILD_VERSION=0.1.0 -DBUILD_PYTHON=ON -DINSTALL_PYTHON=ON .. \
    && cmake --build . \
    && cmake --install .

# Install Python requirements
RUN pip install -r requirements.txt

# Run the main script
CMD [ "python", "src/marketmakingarbitrage/market_making_arbitrage.py" ]