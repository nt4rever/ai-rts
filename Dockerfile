FROM python:3.9.18-slim

RUN apt-get update && apt-get install -y curl

RUN pip install --upgrade pip

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN mkdir /code/store
RUN curl -L -o /code/store/rts.h5 https://minio.hmmmm.tech/hmmmm/models/rts.h5
RUN curl -L -o /code/store/rts_best_weight.h5 https://minio.hmmmm.tech/hmmmm/models/rts_best_weight.h5
COPY ./app.py /code/app.py
COPY ./utils.py /code/utils.py

EXPOSE 8888

CMD ["python", "app.py"]