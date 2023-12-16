CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    admin BOOLEAN NOT NULL,
    created TIMESTAMP NOT NULL,
    modified TIMESTAMP
);

CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    location JSON,
    opening_hours TEXT,
    visible BOOLEAN NOT NULL,
    created TIMESTAMP NOT NULL,
    modified TIMESTAMP
);

CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    stars INT NOT NULL,
    comment TEXT,
    visible BOOLEAN NOT NULL,
    created TIMESTAMP NOT NULL,
    modified TIMESTAMP,
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_restaurant FOREIGN KEY(restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE
);

CREATE TABLE categories ( 
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    created TIMESTAMP NOT NULL,
    modified TIMESTAMP
);

CREATE TABLE restaurants_categories ( 
    restaurant_id INT NOT NULL,
    category_id INT NOT NULL,
	time TIMESTAMP,
    CONSTRAINT fk_restaurant FOREIGN KEY(restaurant_id) REFERENCES restaurants (id) ON DELETE CASCADE,
    CONSTRAINT fk_group FOREIGN KEY(category_id) REFERENCES categories (id) ON DELETE CASCADE,
    UNIQUE (restaurant_id, category_id)
);

CREATE TABLE visits ( 
    user_id INT NOT NULL,
    time TIMESTAMP,
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE images ( 
    name VARCHAR(255),
    data BYTEA,
    time TIMESTAMP,
    restaurant_id INT,
    CONSTRAINT fk_restaurant FOREIGN KEY(restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE
); 

INSERT INTO users (username,password,admin,created) values ('admin','scrypt:32768:8:1$UVpsTmlX8uy8o9N3$0632e6ac194d1e32ca62ae3786fa73c85207f06947cc922a2c36dc106e8ec3ff1b14e806842af38f0678ff559ca66a642de2481607fbd07ea23ecbf45e104690',true, now());