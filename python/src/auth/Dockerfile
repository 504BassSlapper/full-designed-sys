FROM python:3.10-slim-bullseye

RUN apt-get update \
	&& apt-get install -y --no-install-recommends --no-install-suggests \
	build-essential default-libmysqlclient-dev pkg-config  \ 
	&& pip install --no-cache-dir --upgrade pip 
WORKDIR /app
COPY ./requirements.txt /app
## do this last in separate layer in order to build separately this layer
RUN  pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app
EXPOSE 5000
CMD ["python3", "server.py"]

