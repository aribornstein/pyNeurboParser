FROM yujioshima/dynet:base-in-cpp

# DyNet, version 4234759
ENV DYNET_VERSION 4234759
RUN cd /opt && \
        git clone https://github.com/clab/dynet.git && \
        cd dynet && \
        git checkout master && \
        sed -i -e '/^#/!s/ -march=native//g' CMakeLists.txt && \
        mkdir build && \
        cd build && \
        cmake .. -DEIGEN3_INCLUDE_DIR=/opt/eigen && \
        make -j2 install
WORKDIR /opt/dynet

# Clone and build neurbo 
RUN git clone https://github.com/Noahs-ARK/NeurboParser.git
WORKDIR /opt/dynet/NeurboParser

# Install dependencies
RUN git submodule update --init && ./install_deps.sh

# Make NeurboParser
RUN mkdir -p NeurboParser/build   
WORKDIR /opt/dynet/NeurboParser/NeurboParser/build
RUN cmake ..; make -j4
WORKDIR /opt/dynet/NeurboParser

# install zip python and pip
RUN apt-get update && apt-get install zip software-properties-common — no-install-recommends -y &&\
        add-apt-repository ppa:deadsnakes/ppa &&\
        apt-get update && apt-get install python3.6 curl — no-install-recommends -y &&\
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py &&\
        python get-pip.py &&\
# Clean
        apt-get remove curl &&\
        apt-get clean


# Install spacy, flask, conllu
RUN pip install -U spacy &&\
        python -m spacy download en &&\
        pip install flask conllu

# Unzip sdp_models
CMD  unzip /data/pretrained_models/sdp_models.zip && /bin/bash
