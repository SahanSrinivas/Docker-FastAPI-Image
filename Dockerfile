FROM python:3.9  
LABEL app="Boto3 Integration with FastAPI"
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
