FROM php:8.2-cli AS base

# 1. Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    unzip \
    supervisor

RUN docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd

# 2. Install Composer dependencies
FROM base AS composer-install
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer
WORKDIR /app

# Copy composer files and artisan needed for post-install scripts
COPY composer.json composer.lock artisan ./
COPY bootstrap ./bootstrap
COPY config ./config
COPY database ./database
COPY routes ./routes

RUN composer install --no-dev 

# 3. Copy application source
FROM base AS app
WORKDIR /app
COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY --from=composer-install /app/vendor ./vendor
COPY . .

CMD ["bash", "-c", "php artisan migrate --force && exec supervisord"]