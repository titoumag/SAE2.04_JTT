DROP TABLE IF EXISTS coupons;
DROP TABLE IF EXISTS mails;
DROP TABLE IF EXISTS avis;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS panier;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS casque;
DROP TABLE IF EXISTS modele;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS taille;
DROP TABLE IF EXISTS fabricant;
DROP TABLE IF EXISTS couleur;
DROP TABLE IF EXISTS type_casque;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS type_livraison;
DROP TABLE IF EXISTS adresse;
DROP TABLE IF EXISTS couleur;
DROP TABLE IF EXISTS taille;

CREATE TABLE IF NOT EXISTS taille(
   id int auto_increment,
   libelle varchar(20),

    primary key(id)
);

CREATE TABLE IF NOT EXISTS couleur(
    id int auto_increment,
   libelle varchar(20),

    primary key(id)
);

CREATE TABLE IF NOT EXISTS adresse(
    id INT NOT NULL auto_increment,
    user_id int,
    ville VARCHAR(50),
    rue VARCHAR(100),
    numero int,
    code char(5),

    primary key(id)
);



CREATE TABLE IF NOT EXISTS type_livraison(
    id INT NOT NULL auto_increment,
    libelle VARCHAR(50),
    valeurAjoute NUMERIC(4,2),
    PRIMARY KEY(id)
);

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
    solde decimal(12,2),

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
    type_livraison_id INT,
    adresse_id_livraison INT,
    adresse_id_facturation INT,
    clic INT,
    reduction INT,

    CONSTRAINT fk_commande_type_livraison
        FOREIGN KEY(type_livraison_id) REFERENCES type_livraison(id),
    CONSTRAINT fk_commande_user
        FOREIGN KEY(user_id) REFERENCES user(id),
    CONSTRAINT fk_commande_etat
        FOREIGN KEY(etat_id) REFERENCES etat(id),
    CONSTRAINT fk_commande_livraison
        FOREIGN KEY(adresse_id_livraison) REFERENCES adresse(id),
    CONSTRAINT fk_commande_facturation
        FOREIGN KEY(adresse_id_facturation) REFERENCES adresse(id),
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

CREATE TABLE IF NOT EXISTS modele(
    id int auto_increment,
    libelle varchar(50),
    fabricant_id INT NOT NULL,
    type_casque_id INT NOT NULL,
    image VARCHAR(255),
    prix DECIMAL(5,2),
    description VARCHAR(255),

    primary key (id),
    CONSTRAINT fk_modele_fabriquant
       FOREIGN KEY(fabricant_id) REFERENCES fabricant(id),
    CONSTRAINT fk_modele_type
       FOREIGN KEY(type_casque_id) REFERENCES type_casque(id)
);


CREATE TABLE IF NOT EXISTS casque(
   id int auto_increment,
   modele_id int not null,
   -- libelle VARCHAR(50),
   -- image VARCHAR(255),
   stock INT,
   -- prix DECIMAL(5,2),
   -- fabricant_id INT NOT NULL,
   taille_id INT NOT NULL,
   couleur_id INT NOT NULL,
   -- type_casque_id INT NOT NULL,
   -- description VARCHAR(255),

   CONSTRAINT fk_casque_taille
       FOREIGN KEY(taille_id) REFERENCES taille(id),
   CONSTRAINT fk_casque_couleur
        FOREIGN KEY(couleur_id) REFERENCES couleur(id),
    CONSTRAINT fk_casque_mode
        FOREIGN KEY(modele_id) REFERENCES modele(id),

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
    owner_id INT,
    sender_id INT,
    receiver_id INT,
    objetMail varchar(255),
    texteMail varchar(255),
    dateEnvoi DATE,
    PRIMARY KEY(id),
    CONSTRAINT fk_mail_owner
       FOREIGN KEY(owner_id) REFERENCES user(id),
    CONSTRAINT fk_mail_sender
       FOREIGN KEY(sender_id) REFERENCES user(id),
    CONSTRAINT fk_mail_receiver
       FOREIGN KEY(receiver_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS coupons(
  id INT NOT NULL auto_increment,
  valeur INT,
  user_id INT,
  CONSTRAINT fk_coupons_user
    FOREIGN KEY(user_id) REFERENCES user(id),
  PRIMARY KEY (id)
);

INSERT INTO adresse VALUE
    (null,2,'Belfort','rue au hasard',10,'90000'),
    (null,2,'Besancon','boulevard',5,'25000'),
    (null,2,'Paris','rue',2,'75001'),
    (null,2,'Bretigney','rue',3,'25250'),
    (null,3,'Bordeaux','avenue ...',11,'33000');


INSERT INTO type_livraison(libelle,valeurAjoute) VALUES
('Normal',1.0),
('Supplément McDonald',1.2),
('Livraison Express Pierre',1.5),
('Garder Baptiste pour une reduction',0.5),
('Livraison par le gérant de eCasques',5.0);

insert into etat values
(null,'en cours'),
(null,'validé');

INSERT INTO user (email, username,nom,prenom, password, role,  est_actif,solde) VALUES
('admin@admin.fr', 'admin','admin','admin', 'sha256$pBGlZy6UukyHBFDH$2f089c1d26f2741b68c9218a68bfe2e25dbb069c27868a027dad03bcb3d7f69a', 'ROLE_admin', 1,0),
('client@client.fr', 'client','client','client', 'sha256$Q1HFT4TKRqnMhlTj$cf3c84ea646430c98d4877769c7c5d2cce1edd10c7eccd2c1f9d6114b74b81c4', 'ROLE_client', 1,0),
('client2@client2.fr', 'client2','client2','client2', 'sha256$ayiON3nJITfetaS8$0e039802d6fac2222e264f5a1e2b94b347501d040d71cfa4264cad6067cf5cf3', 'ROLE_client', 1,0);


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


INSERT INTO modele(libelle,fabricant_id,type_casque_id,image,prix,description) VALUES
('Casque à pointe',1,1,'casquePointe.png',100.99,'Donne du piquant à la vie'),
('Casque Dragon',3,1,'casqueDragon.png',49.99,'FUS RO DA'),
('Casque (Bon état)',2,3,'casqueFendu1.jpg',10.99,'En très bon état'),
('Casque Allemand',1,1,'casqueFendu2.jpg',61.99,'Parfait pour les amateurs du reich'),
('Casque Gamer METAL',2,2,'casqueGamer.png',5.99,'Enfin un casque pour les gamers métaleux'),
('Casque Gamer Néon',4,2,'CasqueGamer1.jpg',13.99,'Un casque Gamer avec des néons multicolores'),
('Casque Gamer Epic',4,2,'CasqueGamer2.jpg',14.99,'Un casque Gamer totalement épique pour aucune raison'),
('Casque Gamer Disco',4,2,'CasqueGamer3.jpg',10.99,'Un casque Gamer capable d\'éblouir n \'importe qui'),
('Casque Marin',5,3,'casqueMarin.jpeg',75.99,'Parfait pour imiter Tintin et Hadock'),
('Casque Templier',6,1,'casqueMedieval1.jpg',40.99,'DEUS VULT'),
('Haume Viking',7,1,'casqueMedieval2.jpg',20.99,'Parfait pour aller en Norvège'),
('Casque Viking',7,1,'casqueMedieval3.jpg',23.99,'Parfait pour envhair la Grande Bretagne'),
('Casque Chevalier',6,1,'casqueMedieval4.jpg',80.99,'Utilse pour des joutes'),
('Casque Chien',9,3,'casqueAnimal1.jpg',10.99,'Faites parler votre animal intérieur'),
('Casque Chantier',10,3,'casqueChantier1.jpg',15.99,'Pour vous protéger'),
('Casque Contremaitre',10,3,'casqueChantier2.jpg',17.99,'Protège mieux que le casque Chantier'),
('Casque Colonial',8,3,'casqueColonial.jpg',8.99,'Parfait pour explorer l\'Afrique'),
('Casque GIGN',11,1,'casqueMilitaire1.jpg',25.99,'Ne permet pas de devenir agent du GIGN'),
('Casque Soviétique',12,3,'casqueMilitaire2.jpg',18.99,'Parfait pour envahir l\'Afghanistan ou l\'Ukraine'),
('Casque Chat',9,2,'CasqueMusique1.jpg',3.99,'Un casque parfait pour les chat et autres canidés'),
('Casque Wookie',9,2,'CasqueMusique2.jpg',8.99,'Un casque poilant'),
('Casque Musique Pas Fun',9,2,'CasqueMusique3.jpg',4.99,'Un casque sans rien de spécial'),
('Casque de Noel',9,3,'casqueNoel.jpg',31.99,'Avec ce casque, vous pourrez enfin entrer par la cheminé'),
('Casque Pompier',11,3,'casquePompier.jpg',50.99,'Ce casque ne vous permet pas de devenir pompier'),
('Casque Spartiate',8,1,'casqueSparte1.jpg',67.99,'THIS IS SPARTA'),
('Casque Rebelle',13,4,'CasqueStarWars1.jpeg',34.99,'Utile pour les conventions Geek'),
('Casque SotrmTrooper',13,4,'CasqueStarWars2.jpeg',51.99,'Amélliore votre précision de -99%'),
('Casque Kilo Ren',13,4,'CasqueStarWars3.jpeg',37.99,'Permet de perdre 5 kilos'),
('Casque VR Sony',8,5,'casqueVR1.jpg',105.99,'Un casque VR par Sony'),
('Casque LaserScope',8,5,'laserScope.jpg',98.99,'FIRE FIRE FIRE'),
('Occulus Rift',8,5,'occulusRift.jpeg',352.99,'Un autre casque VR'),
('PediSedate (Game Boy)',8,5,'pediSedate.jpeg',67.99,'Utile pour anesthésier des gens'),
('Passoir Pastafariste',9,3,'casquePassoir.png',48.99,'Casque du parfait adorateur des pâtes'),
('Picole Nationale',9,3,'casquePicole.png',36.99,'Casque officel des forces de l\'ordre'), -- '
('Casque Power Ranger',9,3,'casquePowerRanger.png',53.99,'Ce casque est le ranger Jaune devant, Marron derrière'),
('Casque Romain',6,1,'casqueRomain.jpeg',89.99,'C\'est une antiquité qui vaut cher'), -- '
('Casque Samurai',5,1,'casqueSamurai.png',168.99,'La chute des samurais est proche'),
('Casque Dark Vador',13,4,'casqueVador.jpg',75.99,'Vous allez être trop dark avec ce casque'),
('Casque Ailettes',3,1,'casqueEpic1.png',258.99,'C\'est beau ça...'), -- '
('Casque Garde',3,1,'casqueSkyrim1.png',142.99,'Casque de garde'),
('Casque Sommeil',3,1,'CasqueSkyrim2.jpeg',274.99,'Casque pour dormir tout en se protégant'),
('Casque Ponpon',9,3,'CasquePonpon.jpg',29.99,'Casque avec ponpon'),
('Casque Anglais',1,3,'casqueAnglais.jpg',139.99,'Casque officiel de la garde de la reine'),
('Casque Invisible',8,3,'casqueInvisible.png',896.99,'Vous ne verrez aucune rayures dessus !'),
('Casque Batman',9,3,'casqueBatman.jpg',68.99,'Le casque n\'est pas livré avec la cape');

INSERT INTO casque(modele_id,stock,taille_id,couleur_id) VALUES
(1, 47, 3, 1),
(2, 35, 2, 6),
(3, 49, 1, 5),
(4, 47, 1, 4),
(5, 42, 1, 2),
(6, 49, 1, 2),
(7, 29, 2, 3),
(8, 49, 1, 5),
(9, 32, 2, 4),
(10, 43, 2, 5),
(11, 25, 3, 3),
(12, 27, 3, 2),
(13, 25, 3, 6),
(14, 41, 2, 7),
(15, 45, 2, 7),
(16, 30, 2, 5),
(17, 43, 2, 2),
(18, 41, 2, 4),
(19, 46, 1, 4),
(20, 30, 3, 6),
(21, 30, 2, 2),
(22, 49, 1, 6),
(23, 40, 2, 3),
(24, 43, 2, 2),
(25, 31, 2, 4),
(26, 50, 3, 1),
(27, 32, 1, 5),
(28, 50, 2, 3),
(29, 34, 1, 5),
(30, 31, 2, 1),
(31, 49, 1, 4),
(32, 44, 2, 2),
(33, 36, 1, 1),
(34, 50, 1, 5),
(35, 39, 1, 5),
(36, 30, 1, 4),
(37, 38, 3, 5),
(38, 45, 2, 2),
(39, 25, 2, 1),
(40, 33, 2, 2),
(41, 40, 1, 4),
(42, 33, 1, 6),
(43, 47, 1, 7),
(44, 42, 3, 5),
(45, 35, 2, 2);
