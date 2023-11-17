DROP TABLE IF EXISTS images;
DROP TABLE IF EXISTS visits;
DROP TABLE IF EXISTS restaurants_groups;
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS restaurants;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
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

CREATE TABLE groups ( 
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    created TIMESTAMP NOT NULL,
    modified TIMESTAMP
);

CREATE TABLE restaurants_groups ( 
    restaurant_id INT NOT NULL,
    group_id INT NOT NULL,
    CONSTRAINT fk_restaurant FOREIGN KEY(restaurant_id) REFERENCES restaurants (id) ON DELETE CASCADE,
    CONSTRAINT fk_group FOREIGN KEY(group_id) REFERENCES groups (id) ON DELETE CASCADE
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
INSERT INTO users (username,password,admin,created) values ('user','scrypt:32768:8:1$0FzG9yArxzL5krp2$52613cae8b3bcd3a40dc9d5352a27af65f0ef0c9ec61aea6f961961ccb4dc447e9b562dea2e68e73adefe8f2eb49f8858c7e467714f6b5413e2d4a397462cfcd',false, now());