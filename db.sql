
-- 1. Создание пользователя
CREATE USER agent WITH PASSWORD 'BywPCL27';

-- 2. Создание базы данных
CREATE DATABASE medialibrary
    OWNER agent;

-- 3. Назначить права (на всякий случай, если не указан owner)
GRANT ALL PRIVILEGES ON DATABASE medialibrary TO agent;

-- 4. Создание таблицы
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    type TEXT,
    year INT,
    genre TEXT,
    rating DECIMAL(3, 1)
);

-- 5. Удаление таблицы
DROP TABLE movies;