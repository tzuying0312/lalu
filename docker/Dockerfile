FROM python:3.6.2

ENV PYTHONUNBUFFERED 1


RUN mkdir /docker_api
WORKDIR /docker_api
ADD requirements.txt /docker_api/requirements.txt 
RUN pip install -r requirements.txt
RUN apt-get update && apt-get -y install cron
RUN apt-get install -y libav-tools

# Copy hello-cron file to the cron.d directory
COPY hello-cron /etc/cron.d/hello-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/hello-cron

# Apply cron job
RUN crontab /etc/cron.d/hello-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

ADD improve.py /docker_api/improve.py
ADD apikey.json /docker_api/apikey.json

CMD ["cron", "-f"]

RUN echo "Asia/Taipei" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

# ADD entrypoint.sh /docker_api/entrypoint.sh
# RUN chmod 777 /docker_api/entrypoint.sh
# ENTRYPOINT ["/docker_api/entrypoint.sh"]

# Run the command on container startup
#CMD cron && tail -f /var/log/cron.log
#CMD /usr/sbin/cron -f
#RUN service cron start
#RUN cron
#CMD /usr/sbin/cron -f