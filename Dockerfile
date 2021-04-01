FROM ubuntu:20.04

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev libxml2-dev libxslt-dev libffi-dev ffmpeg
    
COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

ENV FILLOABOT_DB_PATH=/etc/filloabot/database.db

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]

