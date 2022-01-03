FROM python:3.8.9

COPY requirements.txt /
RUN pip install -r requirements.txt

CMD [ "python", "src/main.py" ]