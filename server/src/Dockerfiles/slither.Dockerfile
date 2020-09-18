FROM ubuntu:18.04

LABEL name slither
LABEL src "https://github.com/trailofbits/slither"
LABEL creator trailofbits
LABEL dockerfile_maintenance trailofbits
LABEL desc "Static Analyzer for Solidity"

RUN apt update \
  && apt upgrade -y \
  && apt install -y git python3 python3-setuptools python3-pip wget software-properties-common curl

RUN wget https://github.com/ethereum/solidity/releases/download/v0.4.25/solc-static-linux \
  && chmod +x solc-static-linux \
  && mv solc-static-linux /usr/bin/solc


# If this fails, the solc-static-linux binary has changed while it should not.
RUN [ "c9b268750506b88fe71371100050e9dd1e7edcf8f69da34d1cd09557ecb24580  /usr/bin/solc" = "$(sha256sum /usr/bin/solc)" ]


RUN \
  git clone https://github.com/crytic/slither.git
WORKDIR /slither

RUN python3 setup.py install --user
ENV PATH="/root/.local/bin:${PATH}"
CMD /bin/bash

RUN \
  git clone https://github.com/crytic/solc-select.git
RUN cd solc-select/scripts && sh ./install.sh
ENV PATH="/root/.solc-select:${PATH}"


RUN mkdir output
