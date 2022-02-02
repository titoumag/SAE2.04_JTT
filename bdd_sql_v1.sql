DROP TABLE IF EXISTS mails;
DROP TABLE IF EXISTS avis;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS panier;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS casque;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS taille;
DROP TABLE IF EXISTS fabricant;
DROP TABLE IF EXISTS couleur;
DROP TABLE IF EXISTS type_casque;
DROP TABLE IF EXISTS etat;

CREATE TABLE IF NOT EXISTS etat(
    id int auto_increment,
    libelle varchar(20),
    PRIMARY KEY(id)
)character set 'utf8';

CREATE TABLE IF NOT EXISTS user(
    id int auto_increment,

    username varchar(255),
    nom varchar(50),
    prenom varchar(50),
    pseudo varchar(255),
    email varchar(255),
    solde decimal(10,2),
    carte_numero char(16),

    carte_code char(4),
    password varchar(255),

    role varchar(50),
    est_actif tinyint(1),

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
   libelle VARCHAR(50),
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


CREATE TABLE IF NOT EXISTS casque(
   id int auto_increment,
   libelle VARCHAR(50),
   image VARCHAR(50),
   stock INT,
   prix DECIMAL(5,2),
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
--    prix_unit DECIMAL(15,2),
   quantite int,
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
   quantite int,

   CONSTRAINT fk_ligne_commande_commande
       FOREIGN KEY(commande_id) REFERENCES commande(id),
   CONSTRAINT fk_ligne_commande_casque
       FOREIGN KEY(casque_id) REFERENCES casque(id),
   PRIMARY KEY(commande_id, casque_id)
)character set 'utf8';

CREATE TABLE IF NOT EXISTS avis(
    casque_id INT NOT NULL,
    user_id INT NOT NULL,
    texte VARCHAR(255),
    note INT,
    PRIMARY KEY(casque_id,user_id),
   CONSTRAINT fk_avis_casque
       FOREIGN KEY(casque_id) REFERENCES casque(id),
   CONSTRAINT fk_avis_user
       FOREIGN KEY(user_id) REFERENCES user(id)
)character set 'utf8';

CREATE TABLE IF NOT EXISTS mails(
    id INT NOT NULL auto_increment,
    sender_id INT,
    receiver_id INT,
    objetMail varchar(255),
    texteMail varchar(255),
    dateEnvoi DATE,
    PRIMARY KEY(id),
    CONSTRAINT fk_mail_sender
       FOREIGN KEY(sender_id) REFERENCES user(id),
    CONSTRAINT fk_mail_receiver
       FOREIGN KEY(receiver_id) REFERENCES user(id)
);

insert into etat values
(null,'en cours'),
(null,'validé');

INSERT INTO user (email, username,nom,prenom, password, role,  est_actif,solde,carte_numero,carte_code) VALUES
('admin@admin.fr', 'admin','admin','admin', 'sha256$pBGlZy6UukyHBFDH$2f089c1d26f2741b68c9218a68bfe2e25dbb069c27868a027dad03bcb3d7f69a', 'ROLE_admin', 1,0,0000000000000000,'1234'),
('client@client.fr', 'client','client','client', 'sha256$Q1HFT4TKRqnMhlTj$cf3c84ea646430c98d4877769c7c5d2cce1edd10c7eccd2c1f9d6114b74b81c4', 'ROLE_client', 1,0,0100010000100010,'1234'),
('client2@client2.fr', 'client2','client2','client2', 'sha256$ayiON3nJITfetaS8$0e039802d6fac2222e264f5a1e2b94b347501d040d71cfa4264cad6067cf5cf3', 'ROLE_client', 1,0,0200448056200082,'1234');

INSERT INTO fabricant(nom,adresse) VALUES
('Deutschland !','Berlin'),
('Moto MC','Los Angeles'),
('ForgeCiel','Blancherive'),
('Gaming Inc.','Washington DC'),
('Hadock Inc.','Moulinsart'),
('DEUS VULT','Jerusalem'),
('Thor','Oslo'),
('Paradox Inc.','Stockholm'),
('Fun Casque','Paris'),
('Constructor','Prague'),
('Airsoft','Texas'),
('Mère Patrie','Moscou'),
('LucasArt','San Fransisco');

INSERT INTO taille(libelle) VALUES
('Petit'),
('Moyen'),
('Grand');

INSERT INTO couleur(libelle) VALUES
('Gris'),
('Noir'),
('Rouge'),
('Jaune'),
('Marron'),
('Bleu'),
('Rose');

INSERT INTO type_casque(libelle) VALUES
('Militaire'),
('Musique'),
('Protection'),
('Star Wars'),
('Jeu Vidéo');

INSERT INTO casque(libelle,fabricant_id,taille_id,couleur_id,type_casque_id,image,stock,prix) VALUES
('Casque à pointe',1,2,1,1,'casquePointe.png',5,100.99),
('Casque Dragon',3,2,1,1,'casqueDragon.png',15,49.99),
('Casque (Bon état)',2,2,1,3,'casqueFendu1.jpg',75,10.99),
('Casque Allemand',1,2,2,1,'casqueFendu2.jpg',25,61.99),
('Casque Gamer METAL',2,2,2,2,'casqueGamer.png',50,5.99),
('Casque Gamer Néon',4,2,3,2,'CasqueGamer1.jpg',3,13.99),
('Casque Gamer Epic',4,2,1,2,'CasqueGamer2.jpg',10,14.99),
('Casque Gamer Disco',4,2,1,2,'CasqueGamer3.jpg',12,10.99),
('Casque Marin',5,3,4,3,'casqueMarin.jpeg',36,75.99),
('Casque Templier',6,2,1,1,'casqueMedieval1.jpg',54,40.99),
('Haume Viking',7,3,1,1,'casqueMedieval2.jpg',60,20.99),
('Casque Viking',7,2,1,1,'casqueMedieval3.jpg',47,23.99),
('Casque Chevalier',6,1,4,1,'casqueMedieval4.jpg',50,80.99),
('Casque Chien',9,1,5,3,'casqueAnimal1.jpg',7,10.99),
('Casque Chantier',10,2,6,3,'casqueChantier1.jpg',32,15.99),
('Casque Contremaitre',10,2,4,3,'casqueChantier2.jpg',25,17.99),
('Casque Colonial',8,2,5,3,'casqueColonial.jpg',45,8.99),
('Casque GIGN',11,2,1,1,'casqueMilitaire1.jpg',37,25.99),
('Casque Soviétique',12,2,2,1,'casqueMilitaire2.jpg',28,18.99),
('Casque Chat',9,2,7,2,'CasqueMusique1.jpg',48,3.99),
('Casque Wookie',9,2,6,2,'CasqueMusique2.jpg',150,8.99),
('Casque Musique Pas Fun',9,2,2,2,'CasqueMusique3.jpg',21,4.99),
('Casque de Noel',9,2,3,3,'casqueNoel.jpg',15,31.99),
('Casque Pompier',11,2,5,3,'casquePompier.jpg',45,50.99),
('Casque Spartiate',8,2,4,1,'casqueSparte1.jpg',28,67.99),
('Casque Rebelle',13,3,5,4,'CasqueStarWars1.jpeg',78,34.99),
('Casque SotrmTrooper',13,3,1,4,'CasqueStarWars2.jpeg',55,51.99),
('Casque Kilo Ren',13,3,2,4,'CasqueStarWars3.jpeg',48,37.99),
('Casque VR Sony',8,2,2,5,'casqueVR1.jpg',13,105.99),
('Casque LaserScope',8,2,1,5,'laserScope.jpg',28,98.99),
('Occulus Rift',8,2,2,5,'occulusRift.jpeg',27,352.99),
('PediSedate (Game Boy)',8,2,2,5,'pediSedate.jpeg',27,67.99);

INSERT INTO avis VALUES
(1,2,'Incroyable',5);