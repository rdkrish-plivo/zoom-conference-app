# zoom-conference-image
#
# Build it using docker build --no-cache --rm --tag "zoom-conference-image:0.0.1" .
# Run it using docker run --name "zoom-conference" -d -p 5000:5000 -v /path/to/zoom-conference-app/:/zoom-conference-app/ zoom-conference-image:0.0.1
#
# 	Created On: 25-Nov-2016
# 	Last Updated On: 25-Nov-2016
# 	Created By: Radhakrishna Nayak
FROM ubuntu:14.04
MAINTAINER Radhakrishna Nayak radhakrishna@plivo.com

RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install python vim python-pip
RUN pip install plivo flask configobj
ADD ./start-conference-app /

EXPOSE 5000
CMD './start-conference-app'
