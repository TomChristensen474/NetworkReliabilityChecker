# syntax=docker/dockerfile:1
FROM ubuntu:24.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip

COPY requirements.txt /
RUN pip install -r requirements.txt --break-system-packages

COPY src / 
# RUN python3 setup_database.py
# docker runs all commands as superuser by default so ping should work


# final configuration
EXPOSE 8000
# one command to setup database, set up runner and create localserver
CMD ["python3", "runner.py"]