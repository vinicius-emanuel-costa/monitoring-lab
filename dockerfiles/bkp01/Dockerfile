FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Sao_Paulo

RUN apt-get update && apt-get install -y \
    openssh-server \
    cron \
    rsync \
    iproute2 \
    iputils-ping \
    net-tools \
    curl \
    nano \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /run/sshd
ARG ROOT_PASSWORD=changeme
RUN echo "root:${ROOT_PASSWORD}" | chpasswd

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
