FROM ubuntu:20.04
COPY . /app
WORKDIR /app
ENV LANG C.UTF-8
ENV TZ Asia/Tokyo
ENV PIPENV_VENV_IN_PROJECT 1
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      ufw \
      python3.9-dev \
      python3-pip \
      libpq-dev \
      nginx \
      postgresql \
      postgresql-contrib \
    && apt-get -y autoremove \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install pipenv \
    && rm -rf Pipfile.lock db.sqlite3 .venv .vscode
RUN pipenv install \
    && pipenv run python3.9 manage.py collectstatic --no-input \
    && pipenv run python3.9 manage.py migrate
