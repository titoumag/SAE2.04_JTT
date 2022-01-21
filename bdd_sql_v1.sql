DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS etat;

CREATE TABLE etat(
    id int auto_increment,
    libelle varchar(50),
    PRIMARY KEY(id)
);

CREATE TABLE user(
    id int auto_increment,
    username varchar(255),
    password varchar(255),
    role varchar(255),
    est_actif tinyint(1),
    pseudo varchar(255),
    email varchar(255),
    PRIMARY KEY(id)
);

CREATE TABLE commande(
    id int auto_increment,
    date_achat DATE,
    user_id int,
    etat_id int,

    CONSTRAINT fk_commande_user
        FOREIGN KEY(user_id) REFERENCES user(id),
    CONSTRAINT fk_commande_etat
        FOREIGN KEY(etat_id) REFERENCES etat(id),
    PRIMARY KEY(id)
);


INSERT INTO user (email, username, password, role,  est_actif) VALUES
('admin@admin.fr', 'admin', 'sha256$pBGlZy6UukyHBFDH$2f089c1d26f2741b68c9218a68bfe2e25dbb069c27868a027dad03bcb3d7f69a', 'ROLE_admin', 1),
('client@client.fr', 'client', 'sha256$Q1HFT4TKRqnMhlTj$cf3c84ea646430c98d4877769c7c5d2cce1edd10c7eccd2c1f9d6114b74b81c4', 'ROLE_client', 1),
('client2@client2.fr', 'client2', 'sha256$ayiON3nJITfetaS8$0e039802d6fac2222e264f5a1e2b94b347501d040d71cfa4264cad6067cf5cf3', 'ROLE_client', 1);
