FROM python:3.8.9

RUN apt update
RUN apt-get install -y swig libssl-dev
RUN apt install -y cmake g++ make 

COPY ccapi /
COPY user_specified_cmake_include.cmake /ccapi
RUN cd ccapi \
    && mkdir binding/build \
    && cd binding/build \
    && cmake -DCMAKE_PROJECT_INCLUDE=user_specified_cmake_include.cmake -DBUILD_VERSION=0.1.0 -DBUILD_PYTHON=ON -DINSTALL_PYTHON=ON .. \
    && cmake --build . \
    && cmake --install .

COPY requirements.txt /
RUN pip install -r requirements.txt

CMD [ "python", "src/main.py" ]