FROM continuumio/miniconda3:latest
WORKDIR /app

RUN  apt-get update \
  && apt-get install -y nano \
  && apt-get install -y fontconfig \
  && rm -rf /var/lib/apt/lists/*


# NOTE: Coment when you dont want download files
#COPY src /app/src
#COPY main.py /app/main.py
#COPY test.py /app/test.py

COPY requirements.txt /app/requirements.txt
RUN python -m pip install "ray[default]"
RUN python -m pip install -r requirements.txt

COPY bin/ /app/bin/
RUN chmod +x bin/.
