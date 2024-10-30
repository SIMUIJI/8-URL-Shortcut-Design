-- init.sql
CREATE TABLE IF NOT EXISTS urls (
    short_url VARCHAR(255) NOT NULL,
    long_url TEXT NOT NULL,
    is_enable INT NOT NULL DEFAULT 1
);
