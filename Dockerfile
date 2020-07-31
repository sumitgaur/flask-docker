FROM frolvlad/alpine-python2:latest
ARG proxy
ENV https_proxy=$proxy \
	LANG=en_US.UTF-8 \
	LC_ALL=en_US.UTF-8
COPY src /apps
WORKDIR /apps
RUN python -V
RUN pip install pipenv && pipenv install
CMD ["sh","/apps/bootstrap.sh"]
