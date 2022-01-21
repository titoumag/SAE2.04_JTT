DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS panier;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS casque;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS taille;
DROP TABLE IF EXISTS fabricant;
DROP TABLE IF EXISTS couleur;
DROP TABLE IF EXISTS type_casque;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS etat;

CREATE TABLE IF NOT EXISTS etat(
    id int auto_increment,
    libelle varchar(20),
    PRIMARY KEY(id)
)character set 'utf8';

CREATE TABLE IF NOT EXISTS user(
    id int auto_increment,
    username varchar(255),
    password varchar(255),
    role varchar(50),
    est_actif tinyint(1),
    pseudo varchar(255),
    email varchar(255),
    PRIMARY KEY(id)
)character set 'utf8';

CREATE TABLE IF NOT EXISTS commande(
    id int auto_increment,
    date_achat DATE,
    user_id int,
    etat_id int,

    CONSTRAINT fk_commande_user
        FOREIGN KEY(user_id) REFERENCES user(id),
    CONSTRAINT fk_commande_etat
        FOREIGN KEY(etat_id) REFERENCES etat(id),
    PRIMARY KEY(id)
)character set 'utf8';

CREATE TABLE IF NOT EXISTS type_casque(
   id int auto_increment,
   libellle VARCHAR(50),
   PRIMARY KEY(id)
)character set 'utf8';

CREATE TABLE IF NOT EXISTS taille(
   id int auto_increment,
   libelle VARCHAR(50),
   PRIMARY KEY(id)
)character set 'utf8';

CREATE TABLE IF NOT EXISTS fabricant(
   id int auto_increment,
   nom VARCHAR(50),
   adresse VARCHAR(50),
   PRIMARY KEY(id)
)character set 'utf8';

CREATE TABLE IF NOT EXISTS couleur(
   id int auto_increment,
   libelle VARCHAR(50),
   PRIMARY KEY(id)
)character set 'utf8';

CREATE TABLE IF NOT EXISTS commande(
   id int auto_increment,
   date_achat DATE,
   user_id INT NOT NULL,
   etat_id INT NOT NULL,

   CONSTRAINT fk_commande_etat
       FOREIGN KEY(etat_id) REFERENCES etat(id),
   CONSTRAINT fk_commande_user
       FOREIGN KEY(user_id) REFERENCES user(id),
   PRIMARY KEY(id)
)character set 'utf8';

CREATE TABLE IF NOT EXISTS casque(
   id int auto_increment,
   N_serie INT,
   fabricant_id INT NOT NULL,
   taille_id INT NOT NULL,
   couleur_id INT NOT NULL,
   type_casque_id INT NOT NULL,

   CONSTRAINT fk_casque_fabriquant
       FOREIGN KEY(fabricant_id) REFERENCES fabricant(id),
   CONSTRAINT fk_casque_taille
       FOREIGN KEY(taille_id) REFERENCES taille(id),
   CONSTRAINT fk_casque_couleur
        FOREIGN KEY(couleur_id) REFERENCES couleur(id),
   CONSTRAINT fk_casque_type
       FOREIGN KEY(type_casque_id) REFERENCES type_casque(id),
   PRIMARY KEY(id)
)character set 'utf8';

CREATE TABLE IF NOT EXISTS panier(
   id int auto_increment,
   date_ajout DATE,
   prix_unit DECIMAL(15,2),
   quantite VARCHAR(50),
   casque_id INT NOT NULL,
   user_id INT NOT NULL,

   CONSTRAINT fk_panier_casque
       FOREIGN KEY(casque_id) REFERENCES casque(id),
    CONSTRAINT fk_panier_user
       FOREIGN KEY(user_id) REFERENCES user(id),
    PRIMARY KEY(id)
)character set 'utf8';

CREATE TABLE IF NOT EXISTS ligne_commande(
   commande_id INT,
   casque_id INT,
   prix_unit DECIMAL(6,2),
   quantite DECIMAL(7,3),

   CONSTRAINT fk_ligne_commande_commande
       FOREIGN KEY(commande_id) REFERENCES commande(id),
   CONSTRAINT fk_ligne_commande_casque
       FOREIGN KEY(casque_id) REFERENCES casque(id),
   PRIMARY KEY(commande_id, casque_id)
)character set 'utf8';



INSERT INTO user (email, username, password, role,  est_actif) VALUES
('admin@admin.fr', 'admin', 'sha256$pBGlZy6UukyHBFDH$2f089c1d26f2741b68c9218a68bfe2e25dbb069c27868a027dad03bcb3d7f69a', 'ROLE_admin', 1),
('client@client.fr', 'client', 'sha256$Q1HFT4TKRqnMhlTj$cf3c84ea646430c98d4877769c7c5d2cce1edd10c7eccd2c1f9d6114b74b81c4', 'ROLE_client', 1),
('client2@client2.fr', 'client2', 'sha256$ayiON3nJITfetaS8$0e039802d6fac2222e264f5a1e2b94b347501d040d71cfa4264cad6067cf5cf3', 'ROLE_client', 1);
