FROM python:3.6.1
MAINTAINER Mike Tung <miketung2013@gmail.com>

COPY ./coder_engine /coder_app/coder_engine
COPY ./app.py /coder_app/app.py
COPY ./requirements.txt /coder_app/requirements.txt
COPY ./settings.py /coder_app/settings.py

WORKDIR /coder_app

RUN pip install -r requirements.txt
RUN echo "I'm done installing requirements"
RUN rm requirements.txt

EXPOSE 3000