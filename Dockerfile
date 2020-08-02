FROM python:2.7-alpine
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev
ARG proxy
ENV https_proxy=$proxy \
	LANG=en_US.UTF-8 \
	LC_ALL=en_US.UTF-8
COPY src /apps
WORKDIR /apps
RUN python -V
RUN pip install pipenv && pipenv install
CMD ["sh","/apps/bootstrap.sh"]