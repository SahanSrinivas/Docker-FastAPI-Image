FROM python:3.9  
LABEL app="Boto3 Integration with FastAPI"
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

ENV AWS_ACCESS_KEY_ID=value
ENV AWS_SECRET_ACCESS_KEY=value

RUN pip install --no-cache-dir --upgrade -r requirements.txt \
    && python --version

COPY main.py /code/main.py
CMD [ "uvicorn","main:app","--host" ,"0.0.0.0","--port","80"]
