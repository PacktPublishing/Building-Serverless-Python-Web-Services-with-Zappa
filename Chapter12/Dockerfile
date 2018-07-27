FROM lambci/lambda:build-python3.6

MAINTAINER "Abdul Wahid" <abdulwahid24@gmail.com>



# Add your extra requirements here
RUN yum install -y wget && \
    pip install pipenv

WORKDIR /doc-parser

# Configure catdoc
RUN cd /tmp && \
    wget http://ftp.wagner.pp.ru/pub/catdoc/catdoc-0.95.tar.gz && \
    tar -xf catdoc-0.95.tar.gz && \
    cd catdoc-0.95/ && \
    ./configure --prefix=/doc-parser/usr/ && \
    make && \
    make install

COPY Pipfile Pipfile
RUN  pipenv install --deploy --system --skip-lock
