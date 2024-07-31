FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED=1 \
PYTHONFAULTHANDLER=1 \
PIP_NO_CACHE_DIR=off \
PIP_DISABLE_PIP_VERSION_CHECK=on \
PIP_DEFAULT_TIMEOUT=120

WORKDIR /app
COPY ./eligibility_model/requirements.txt /app/

RUN apt-get -y update \
&& apt-get -y upgrade \
&& apt-get -y install  curl build-essential syslog-ng \
&& pip install -r requirements.txt \
&& apt remove build-essential -y --purge && apt autoremove -y \
&& rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-c"] 
COPY ./eligibility_model/code /app/

ENTRYPOINT [ "python", "-m", "run" ]
