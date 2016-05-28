FROM ubuntu:latest

# Install dependencies
RUN apt-get update
RUN apt-get install cron
RUN apt-get -y install curl
RUN apt-get -y install openssl


ADD spark/pi.py /spark/pi.py
ADD spark/vcap.json /spark/vcap.json
ADD spark/spark-submit.sh /spark/spark-submit.sh
RUN chmod +x /spark/spark-submit.sh

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/simple-cron

# Add shell script and grant execution rights
ADD script.sh /spark/script.sh
RUN chmod +x /spark/script.sh

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/simple-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log
RUN mkdir /spark-logs/

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
