FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
ADD requirements.pip /config/
RUN pip install -r /config/requirements.pip
RUN mkdir /src
ADD /src /src
WORKDIR /src
EXPOSE 8000
ENV GUNICORN_CMD_ARGS "--bind=0.0.0.0"
ENTRYPOINT ["gunicorn", "PET.wsgi"]
