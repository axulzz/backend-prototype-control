# pull official base image
FROM python:alpine AS base

# Argument variables
ARG SRC_DIR=/usr/src/app
ARG HOME=$SRC_DIR
ARG APP_USER=django
ARG DJANGO_ENV=development

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8
ENV LANG C.UTF-8
ENV HOME=${HOME}
ENV DJANGO_ENV=${DJANGO_ENV}

# Update dependencies tree
RUN apk update

# Install psycopg2, grpc dependencies
RUN apk add --no-cache build-base libffi-dev gettext
# RUN apt-get -y install default-libmysqlclient-dev

# Make sure we have the latest PIP
RUN pip install --upgrade pip

WORKDIR $SRC_DIR

EXPOSE 8000

FROM base AS builder

ARG REQUIREMENTS_FILE=requirements.txt
ARG ENTRYPOINT_FILE=docker-entrypoint.sh


# Install dependencies
COPY ${REQUIREMENTS_FILE} .
RUN pip install --no-cache-dir -r ${REQUIREMENTS_FILE}

# python entrypoint
COPY ./${ENTRYPOINT_FILE} /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

FROM builder AS dev-builder

RUN apk update \
    && apk add --virtual build-deps gcc musl-dev \
    && apk add --no-cache mariadb-dev

ARG DEV_REQUIREMENTS_FILE=requirements.dev.txt

# # Install dependencies
COPY ${DEV_REQUIREMENTS_FILE} .
RUN pip install --no-cache-dir -r ${DEV_REQUIREMENTS_FILE}

FROM dev-builder AS development

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM dev-builder AS development-envs

RUN apk add git
RUN addgroup -S docker
RUN adduser -S --shell /bin/bash --ingroup docker vscode

# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /

ARG DJANGO_ENV=production
FROM builder AS production

# create the app user
RUN addgroup -S ${APP_USER} && adduser -S ${APP_USER} -G ${APP_USER}

# copy project
COPY . .

# lint
RUN pip install flake8==3.9.2
RUN flake8 .

# project structure
RUN mkdir static media

# chown all the files to the app user
RUN chown -R ${APP_USER}:${APP_USER} $SRC_DIR

# change to the app user
USER ${APP_USER}

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]