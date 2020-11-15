FROM nvidia/cuda:11.4.1-cudnn8-runtime-ubuntu20.04

LABEL AUTHOR="Tuan Nguyen-Anh <aifi.cope@gmail.com>"
LABEL SYSTEM="X0036"

RUN apt update -y && apt upgrade -y

RUN apt install -y python3-dev python3-pip

COPY requirements.txt /src/requirements.txt

WORKDIR /src

RUN pip3 install -r requirements.txt

COPY ./python/load_data_from_eventhub_and_process.py /src

COPY ./python/config.json /src

COPY ./models/best.pth /src

CMD [ "python3", "load_data_from_eventhub_and_process.py", "-m /src/best.pth", "-c /src/config.json" ]