FROM python:3.7
MAINTAINER Andrew Smirnov <smirnov@informatics.ru>
ADD ./ /s104_juk
WORKDIR /s104_juk/
RUN apt-get update && apt-get install -y build-essential nano python3-dev libmysqlclient-dev
RUN pip install --no-cache-dir -r ./requirements.txt
CMD exec ./docker/run.sh
