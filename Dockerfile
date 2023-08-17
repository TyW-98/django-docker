# Alphine is lightweight linux OS
FROM python:3.9-alpine3.13 
LABEL maintainer="TyW-98"

ENV PYTHONUNBUFFERED 1

# Copy requirements.txt to tmp/requirements.txt in container
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# Copy app directory to app directory in container
COPY ./app /app
# Set working directory 
WORKDIR /app
# Port which will be exposed when running the container
EXPOSE 8000

# Set build argument DEV = false
ARG DEV=false
# Use "&& \" to break multiple commands when using a single RUN command
# Create new virtual environment
RUN python -m venv /py && \ 
    # Upgrade virtual environment's pip
    /py/bin/pip install --upgrade pip && \
    # Install postgresql adapter (psycopg2) installation dependencies (specific for 13-alpine OS)
    apk add --update --no-cache postgresql-client && \ 
    # Group packages in the directory 
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    # Install packages from requirements.txt
    /py/bin/pip install -r /tmp/requirements.txt && \
    # IF statement to check if DEV = true then install packages from dev requirements
    if [ $DEV = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # remove temporary directory (Since this is not needed after packages are installed)
    rm -rf /tmp && \
    # Remove packages grouped in the directory (Excess packages)
    apk del .tmp-build-deps && \
    # Add new user inside docker image (Avoid using root user, which will be the default user if not created.)
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Will add "/py/bin" to the system path therefore it will run command in the path everytime.
ENV PATH="/py/bin:$PATH"

# Switching to this user so not operating in root user
USER django-user

