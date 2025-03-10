CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    username VARCHAR(100) DEFAULT NULL,  -- Явно разрешаем NULL
    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
