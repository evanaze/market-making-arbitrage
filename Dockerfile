FROM python:3.8.9

RUN apt update
RUN apt-get install -y swig libssl-dev
RUN apt install -y cmake g++ make 

COPY ccapi /

COPY requirements.txt /
RUN pip install -r requirements.txt

CMD [ "python", "src/main.py" ]