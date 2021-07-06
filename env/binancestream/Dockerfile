FROM python:3.8-slim

# ENV GROUP_ID=1000 \
#     USER_ID=1000

WORKDIR /var/www/

# ADD ./requirements.txt /var/www/

RUN apt-get update && apt-get install -y --no-install-recommends git && apt-get purge -y --auto-remove

RUN git clone https://github.com/adriancr/btc-realtime-data.git .
RUN pip install -r requirements.txt
# RUN pip install gunicorn

# RUN addgroup -g $GROUP_ID www
# RUN adduser -D -u $USER_ID -G www www -s /bin/sh

# USER www

EXPOSE 5000

CMD [ "python3", "bin_stream_poc.py"]
