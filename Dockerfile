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

FROM base AS composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer
WORKDIR /app

COPY . .

RUN composer install --no-dev 

# 3. Copy application source
FROM base AS app
WORKDIR /app
COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY --from=composer /app/vendor ./vendor
COPY --from=composer /app/ ./

CMD ["bash", "-c", "php artisan migrate --force && exec supervisord"]