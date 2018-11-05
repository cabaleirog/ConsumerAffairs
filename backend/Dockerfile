FROM python:3.6

LABEL maintainer="Paolo Cabaleiro <cabaleirog@gmail.com>"

# RUN apk add --no-cache \
#     nano \
#     curl

RUN apt-get update && apt-get install -y \
    nano \
    curl

ENV APP_PATH /usr/src/app

RUN mkdir $APP_PATH

WORKDIR $APP_PATH

COPY requirements.txt $APP_PATH

RUN pip install --no-cache-dir -r requirements.txt

COPY . $APP_PATH

EXPOSE 5000

CMD ["python", "-m", "run_server"]
