FROM tensorflow/tensorflow:2.2.2
WORKDIR /app
ADD . /app
COPY ./requirements.txt /var/www/requirements.txt
RUN python3 -m pip install --upgrade pip
EXPOSE 80
RUN pip3 install -r /var/www/requirements.txt
CMD ["python", "app.py"]