FROM python:3.9

RUN mkdir /demo

WORKDIR /demo

COPY requirements.txt /demo/

RUN pip install -r requirements.txt

COPY . /demo/

EXPOSE 5000

CMD [ "python", "/demo/app.py" ]
