FROM python:3.6-slim

RUN apt-get clean \
    && apt-get -y update
RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

COPY . /srv/maths_test
WORKDIR /srv/maths_test

RUN pip install -r requirements.txt --src /usr/local/src
# Install as well so we can use the CLI
RUN pip install .

COPY nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]