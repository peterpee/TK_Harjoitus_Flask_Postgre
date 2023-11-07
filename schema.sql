
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    hashed VARCHAR(255) NOT NULL,
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    cooking_time INTEGER NOT NULL,
    give_rating INTEGER NOT NULL,
    tot_rating INTEGER NOT NULL,
    avg_ratings NUMERIC NOT NULL,
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER NOT NULL,
    ingredient VARCHAR(255) NOT NULL,
    amount DOUBLE NOT NULL,
    unit VARCHAR(255) NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);

CREATE TABLE instructions(
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER NOT NULL,
    instruction VARCHAR NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);

