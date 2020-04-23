FROM python:3.7.3-slim-stretch
RUN apt-get update
RUN apt-get dist-upgrade -y
RUN apt-get install xvfb -y
RUN apt-get install x11-utils -y
RUN apt-get install libgtk2.0-0 -y
RUN pip install pyquery
RUN pip install hanziconv
RUN pip install jieba
RUN pip install requests-html
RUN pip install PyVirtualDisplay
RUN pip install tinydb
WORKDIR /home/NewsFeed
COPY pyppeteer pyppeteer
WORKDIR /home/NewsFeed/pyppeteer
RUN python3 setup.py install
RUN apt-get update && apt-get install -y \
      chromium \
      chromium-l10n \
      fonts-liberation \
      fonts-roboto \
      hicolor-icon-theme \
      libcanberra-gtk-module \
      libexif-dev \
      libgl1-mesa-dri \
      libgl1-mesa-glx \
      libpango1.0-0 \
      libv4l-0 \
      fonts-symbola \
      --no-install-recommends
WORKDIR /root/.local/share/pyppeteer/local-chromium/575458/chrome-linux
RUN ln -s /usr/bin/chromium-browser chrome
RUN apt-get install gconf-service libasound2 libatk1.0-0 libatk-bridge2.0-0 -y
RUN apt-get install libc6 libcairo2 libcups2 libdbus-1-3 -y
RUN apt-get install  libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 -y
RUN apt-get install libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0  -y
WORKDIR /home/NewsFeed