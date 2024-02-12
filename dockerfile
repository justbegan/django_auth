FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y libgdal-dev
RUN pip install GDAL==3.2.2.1
COPY admin_static_files/openlayers.html /usr/local/lib/python3.9/site-packages/django/contrib/gis/templates/gis/
COPY admin_static_files/OLMapWidget.js /usr/local/lib/python3.9/site-packages/django/contrib/gis/static/gis/js/