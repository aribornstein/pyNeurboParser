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
RUN git submodule update --init
RUN ./install_deps.sh
# Make NeurboParser
RUN mkdir -p NeurboParser/build   
WORKDIR /opt/dynet/NeurboParser/NeurboParser/build
RUN cmake ..; make -j4
WORKDIR /opt/dynet/NeurboParser

# install python and 
RUN apt-get update
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install python3.6 -y
RUN apt-get install curl -y
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py
RUN pip install -U spacy && python -m spacy download en

