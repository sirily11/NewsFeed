FROM python:3.7.7
RUN apt-get update
RUN apt-get dist-upgrade -y
RUN apt-get install iceweasel xvfb -y
COPY requirement.txt requirement.txt
RUN pip3 install -r requirement.txt
COPY ./Feed/driver/x86/geckodriver /usr/local/bin/
WORKDIR /home/NewsFeed