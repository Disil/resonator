FROM php:fpm

RUN docker-php-ext-install pdo_mysql

RUN pecl install xdebug && docker-php-ext-enable xdebug

RUN apt-get update && apt-get install -y \
    git \
    unzip \
    curl

COPY --from=composer:latest /usr/bin/composer /usr/local/bin/composer