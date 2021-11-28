FROM python:3.7.7
ENV PYTHONUNBUFFERED 1
WORKDIR /web
COPY . .
RUN pip install -r requirements.txt
CMD ["/bin/bash", "run-server.sh"]