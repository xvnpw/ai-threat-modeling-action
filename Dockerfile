# Container image that runs your code
FROM python@sha256:88880bc85b0e3342ff416c796df7ad9079b2805f92a6ebfc5c84ac582fb25de9

ENV AI_THREAT_MODELING_VERSION=1.0.1

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
