# 3.11.7-alpine
FROM python@sha256:84271da1cd297b01dd4706e01e7789b08b54a5a512c0e3fcaf11c902640f5ebd 

ENV AI_THREAT_MODELING_VERSION=1.1.1

WORKDIR /app

RUN wget -q -O ai-threat-modeling.tar.gz "https://github.com/xvnpw/ai-threat-modeling/archive/refs/tags/v${AI_THREAT_MODELING_VERSION}.tar.gz" && \
    tar -xzvf ai-threat-modeling.tar.gz && \
    rm ai-threat-modeling.tar.gz && \
    mv "ai-threat-modeling-${AI_THREAT_MODELING_VERSION}" ai-threat-modeling

WORKDIR /app/ai-threat-modeling 
RUN pip install --no-cache-dir -r requirements.txt

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]
