FROM python:3.9.18-slim

RUN pip install --upgrade pip

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./store /code/store
COPY ./app.py /code/app.py
COPY ./utils.py /code/utils.py

EXPOSE 8888

CMD ["python", "app.py"]