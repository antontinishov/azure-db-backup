FROM ubuntu:16.04
LABEL maintainer="Anton Tinishov"
ENV install_dir=azure-backup

ENV PYTHONUNBUFFERED 1

RUN find / -perm 6000 -type f -exec chmod a-s {} \; || true && \
    apt-get update -y --no-install-recommends && \
    apt-get install -y wget build-essential libssl-dev libffi-dev && \
    echo "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
    apt-key add - && \
    apt-get update -y --no-install-recommends && \

    apt-get install -y \
    software-properties-common tzdata locales cron postgresql-client-9.6 && \
    add-apt-repository -y ppa:jonathonf/python-3.6 && \
    apt-get update -y --no-install-recommends && \
    apt-get install -y python3.6 python3-pip python3.6-dev&& \
    pip3 install --upgrade pip && \
    rm -rf /var/lib/apt/lists/* && \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 && \
    echo "Europe/Moscow" > /etc/timezone && rm /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

ADD . /docker/$install_dir
RUN python3.6 -m pip install -r /docker/$install_dir/requirements.txt
ENV LANG en_US.utf8

CMD ["/bin/bash", "-c", "python3.6 /docker/$install_dir/main.py"]