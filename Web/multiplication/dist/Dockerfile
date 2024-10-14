FROM php

USER www-data
WORKDIR /var/www/html

USER root
COPY ./src/ .

USER www-data
EXPOSE 8080
CMD php -S 0.0.0.0:8080
