FROM ubuntu
RUN apt-get update
RUN apt-get dist-upgrade -y
RUN apt-get install curl -y
RUN apt-get install wget -y
RUN cd /tmp
RUN df -h
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/miniconda3
RUN /opt/miniconda3/bin/conda init bash
RUN source /opt/miniconda3/bin/activate
RUN conda init --all
RUN conda create --name dist_model -y
RUN conda activate dist_model
RUN conda install python -y
RUN conda install torch transformer langchain langchain-community -y

CMD conda list --reverse