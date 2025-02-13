FROM ubuntu

# Update and install necessary packages
RUN apt-get update && apt-get install -y curl wget

# Download and install Miniconda
RUN curl -o /tmp/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash /tmp/miniconda.sh -b -p ~/conda && \
    rm /tmp/miniconda.sh

# Set environment variables
ENV CONDA_HOME=~/conda
ENV PATH=$CONDA_HOME/bin:$PATH

# Make the environment directory accessible
RUN chmod -R 777 ~/conda

# Create and activate environment, and install packages, all in one RUN command
RUN  /bin/bash -c "conda create -n dist_model -y python=3.9 && \
     source ~/conda/bin/activate dist_model && \
     conda install -y pytorch conda-forge::transformers langchain langchain-community nltk flask fastapi conda-forge::faiss-cpu openai conda-forge::langchain-huggingface && \
     conda info --envs"
RUN apt-get update && apt-get install -y python3-pip git
# Add environment activation to .bashrc (optional, but often helpful for future shell sessions)
RUN echo "source ~/conda/bin/activate dist_model" >> /root/.bashrc
RUN cd ~ && git clone https://github.com/aliakbar1881/dist_model.git && cd dist_model/service/
RUN mkdir ~/dist_model/service/index ~/dist_model/service/data
# Verify environment
CMD ["/bin/bash", "-c", "source ~/conda/bin/activate dist_model && cd ~/dist_model/service/ && echo PYTHONPATH=$PWD >> .env && export PYTHONPATH=$PWD && python main.py"]