FROM python:3.6.1
MAINTAINER Mike Tung <miketung2013@gmail.com>

COPY ./data_engines /coder_app/data_engines
COPY ./security /coder_app/security
COPY ./app.py /coder_app/app.py
COPY ./requirements.txt /coder_app/requirements.txt
COPY ./settings.py /coder_app/settings.py
COPY ./entrypoint.sh /coder_app/entrypoint.sh

WORKDIR /coder_app

RUN pip install -r requirements.txt
RUN rm requirements.txt

ENTRYPOINT ["/coder_app/entrypoint.sh"]