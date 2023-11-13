FROM python:3.8.14

ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.local/bin:$PATH"

# Install dependencies
RUN apt-get update
RUN apt-get install gettext libgettextpo-dev -y
RUN apt-get install libssl-dev -y
RUN apt-get install git -y

RUN openssl genrsa -out jwt_api_key 1024
RUN openssl rsa -in jwt_api_key -pubout -out jwt_api_key.pub

COPY ./api/start.sh /start.sh
RUN chmod +x /start.sh

# Install package
COPY ./api/requirements /requirements
RUN pip install --upgrade pip
RUN pip install -r /requirements/requirement.txt

WORKDIR /usr/src/api
