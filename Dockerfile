FROM python:3.8.9

RUN sudo apt-get install -y swig
RUN sudo apt install -y cmake g++ make 

COPY ccapi /

COPY requirements.txt /
RUN pip install -r requirements.txt

CMD [ "python", "src/main.py" ]