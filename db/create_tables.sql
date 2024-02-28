CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    lastname VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    image_url VARCHAR(255),
    metadata VARCHAR(255),
    scan_results VARCHAR(255),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE invitation (
    id SERIAL PRIMARY KEY,
    invitee_email VARCHAR(255) NOT NULL,
    inviter_user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)


CREATE TABLE apis (
    id SERIAL PRIMARY KEY,
    name  VARCHAR(255) NOT NULL,
    about VARCHAR(255) NOT NULL,
    is_registered BOOLEAN DEFAULT TRUE
);


CREATE TABLE plugins (
    id SERIAL PRIMARY KEY,
    name  VARCHAR(255) NOT NULL,
    about VARCHAR(255) NOT NULL,
    is_registered BOOLEAN DEFAULT TRUE
);