FROM python:3.8.9

# Install 
RUN apt update
RUN apt-get install -y swig libssl-dev
RUN apt install -y cmake>=3.17

# Copy over the directory and make it the primary directory
COPY . /market_making_arbitrage
WORKDIR /market_making_arbitrage

# Build CCAPI
RUN cd ccapi \
    && mkdir binding/build \
    && cd binding/build \
    && cmake -DCMAKE_PROJECT_INCLUDE=../user_specified_cmake_include.cmake -DBUILD_VERSION=0.1.0 -DBUILD_PYTHON=ON -DINSTALL_PYTHON=ON .. \
    && cmake --build . \
    && cmake --install .

# Install the Python requirements
RUN pip install -r requirements.txt

# Run the main script
CMD [ "python", "src/main.py" ]