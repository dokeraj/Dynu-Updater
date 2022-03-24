FROM python:alpine3.14

RUN pip3 install APScheduler
RUN pip3 install Flask
RUN pip3 install environs
RUN pip3 install requests
RUN pip3 install six
RUN pip3 install waitress
RUN pip3 install wheel

RUN mkdir /pyScript

ADD api_controller.py /pyScript/
ADD apiCalls.py /pyScript/
ADD EnvVars.py /pyScript/
ADD main.py /pyScript/
ADD sqliteDatabase.py /pyScript/

WORKDIR /pyScript/

CMD ["python3", "-u", "/pyScript/main.py"]