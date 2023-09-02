FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1
ENV LANG ru_RU.UTF-8

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    git \
    libproj-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY . /code


RUN pip install --no-cache-dir -r requirements.txt

CMD [ "/code/.docker-entrypoint.sh" ]