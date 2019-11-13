FROM java:8

RUN apt-get install wget curl bzip2

RUN curl -sSL https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -bfp /usr/local \
    && rm -rf /tmp/miniconda.sh \
    && conda install -y python=3 \
    && conda update conda \
    && apt-get -qq -y remove curl bzip2 \
    && apt-get -qq -y autoremove \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /var/log/dpkg.log \
    && conda clean --all --yes

ENV PATH /opt/conda/bin:$PATH

WORKDIR /hail/

RUN conda install jupyter && conda install -c conda-forge pyspark

RUN pip install hail


EXPOSE 8889

CMD ["sh", "-c", "jupyter notebook --port=8889 --no-browser --ip=0.0.0.0 --allow-root"]
