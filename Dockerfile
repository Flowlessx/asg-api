FROM ubuntu:21.04

# update ubuntu 
RUN apt-get update   
RUN apt-get upgrade -y
# set debian frontend to non interactive to avoid 
# necesarry user command input
ARG DEBIAN_FRONTEND=noninteractive
# install python , python pip and all build essentials
RUN apt-get -qq install python3-pip python3 build-essential python3-pymysql 
# copy current directory to app folder
COPY . /app
# set app folder as current workdirectory
WORKDIR /app 
# set env variables
ENV FLASK_APP=app.py
# expose  port 
EXPOSE 8080
# use pip to install requirments library
RUN pip install -r requirements.txt
# run flask and set hostname and port for flask app
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "8085"]