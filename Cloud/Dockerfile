FROM raspbian/desktop
USER root
RUN apt update && apt install -y \
	python3-pip \
	apache2 \
	apache2-dev \
	libatlas3-base
RUN pip3 install pandas \
	&& pip3 install dash \
	&& pip3 install dash-bootstrap-components \
	&& pip3 install influxdb \
	&& pip3 install pinform \
	&& pip3 install rfc3339\
	&& pip3 install mod-wsgi \
	&& pip3 install paho-mqtt
WORKDIR /home/pi
COPY . .
RUN chmod a+x start.sh
EXPOSE 8000
USER pi
ENTRYPOINT ["bash", "./start.sh"]



