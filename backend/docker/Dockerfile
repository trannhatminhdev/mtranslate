# Use an official Python runtime as a parent image
FROM continuumio/miniconda3:24.1.2-0

# Set the working directory in the container to /app
WORKDIR /app

# Copy code
COPY openvoice /app/openvoice
COPY docker /app/docker
COPY resources /app/resources

# Set the working directory to OpenVoice
WORKDIR /app/openvoice

# Create a new conda environment with python 3.9 and activate it
RUN conda create -n openvoice python=3.9
RUN echo "source activate openvoice" > ~/.bashrc
ENV PATH=/opt/conda/envs/openvoice/bin:$PATH
# force python to use unbuffered mode for logging
ENV PYTHONUNBUFFERED=1

# Install the OpenVoice package and uvicorn for FastAPI
# Install MeloTTS
RUN git clone https://github.com/myshell-ai/MeloTTS.git && \
  cd MeloTTS && \
  pip install -e . && \
  python -m unidic download && \
  cd ..

RUN pip install -e . uvicorn ffmpeg
RUN pip install -r requirements.txt

# # Download and extract the checkpoint file
RUN apt-get update && apt-get install -y unzip wget libmagic1 libmagic-dev
RUN wget https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip
RUN unzip checkpoints_v2_0417.zip -d /app
RUN rm checkpoints_v2_0417.zip

# Make port 8000 available to the world outside this container
EXPOSE 8000
EXPOSE 7860

RUN cd /app
WORKDIR /app

RUN conda install ffmpeg
RUN conda install --yes -c conda-forge libmagic --solver=classic

# # Provide permissions to execute the script
RUN chmod +x /app/docker/dev.sh
RUN chmod +x /app/docker/start.sh
RUN chmod +x /app/docker/start_and_stop_server.sh
RUN /app/docker/start_and_stop_server.sh
