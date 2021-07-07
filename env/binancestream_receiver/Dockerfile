FROM python:3.8-slim

WORKDIR /var/www/

#Install Git
RUN apt-get update && apt-get install -y --no-install-recommends git && apt-get purge -y --auto-remove

#Get code from repo
RUN cd /var/www && git clone https://github.com/adriancr/btc-realtime-data.git .

#Install requirements
RUN cd binance-stream-receiver && pip3 install -r requirements.txt

# EXPOSE 5000


# We need mongodb configured before running the stream command:

# docker-compose up 
# docker exec -it brd_mongodb /bin/bash
# run "Mongo DB Setup CMDs" from file "some_notes"
# uncomment CMD below
# docker-compose up --build -d

CMD [ "python3", "bin_stream.py"]
