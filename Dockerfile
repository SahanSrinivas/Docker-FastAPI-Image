FROM python:3.9  
LABEL app="Boto3 Integration with FastAPI"
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
ARG T_VERSION=1.7.4


ENV AWS_ACCESS_KEY_ID=value
ENV AWS_SECRET_ACCESS_KEY=value

RUN pip install --no-cache-dir --upgrade -r requirements.txt \
    && python --version && apt update && apt install -y unzip

COPY main.py /code/main.py
ADD Dockerfile.info instructions.txt
ADD https://releases.hashicorp.com/terraform/{T_VERSION}/terraform_{T_VERSION}_linux_amd64.zip terraform.zip
RUN unzip terraform.zip -d /usr/local/bin
CMD [ "uvicorn","main:app","--host" ,"0.0.0.0","--port","80"]