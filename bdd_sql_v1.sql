DROP TABLE IF EXISTS coupons;
DROP TABLE IF EXISTS mails;
DROP TABLE IF EXISTS avis;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS panier;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS casque;
DROP TABLE IF EXISTS liste_adresse;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS taille;
DROP TABLE IF EXISTS fabricant;
DROP TABLE IF EXISTS couleur;
DROP TABLE IF EXISTS type_casque;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS type_livraison;
DROP TABLE IF EXISTS adresse;

CREATE TABLE IF NOT EXISTS adresse(
    id INT NOT NULL auto_increment,
    user_id int,
    ville VARCHAR(50),
    rue VARCHAR(100),
    numero int,
    code int,

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
   description VARCHAR(255),
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
    (null,2,'Belfort','rue au hasard',10,90000),
    (null,2,'Besancon','boulevard',5,25000);


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

INSERT INTO casque(libelle,fabricant_id,taille_id,couleur_id,type_casque_id,image,stock,prix,description) VALUES
('Casque à pointe',1,2,1,1,'casquePointe.png',5,100.99,'Donne du piquant à la vie'),
('Casque Dragon',3,2,1,1,'casqueDragon.png',15,49.99,'FUS RO DA'),
('Casque (Bon état)',2,2,1,3,'casqueFendu1.jpg',75,10.99,'En très bon état'),
('Casque Allemand',1,2,2,1,'casqueFendu2.jpg',25,61.99,'Parfait pour les amateurs du reich'),
('Casque Gamer METAL',2,2,2,2,'casqueGamer.png',50,5.99,'Enfin un casque pour les gamers métaleux'),
('Casque Gamer Néon',4,2,3,2,'CasqueGamer1.jpg',3,13.99,'Un casque Gamer avec des néons multicolores'),
('Casque Gamer Epic',4,2,1,2,'CasqueGamer2.jpg',10,14.99,'Un casque Gamer totalement épique pour aucune raison'),
('Casque Gamer Disco',4,2,1,2,'CasqueGamer3.jpg',12,10.99,'Un casque Gamer capable d\'éblouir n\'importe qui'),
('Casque Marin',5,3,4,3,'casqueMarin.jpeg',36,75.99,'Parfait pour imiter Tintin et Hadock'),
('Casque Templier',6,2,1,1,'casqueMedieval1.jpg',54,40.99,'DEUS VULT'),
('Haume Viking',7,3,1,1,'casqueMedieval2.jpg',60,20.99,'Parfait pour aller en Norvège'),
('Casque Viking',7,2,1,1,'casqueMedieval3.jpg',47,23.99,'Parfait pour envhair la Grande Bretagne'),
('Casque Chevalier',6,1,4,1,'casqueMedieval4.jpg',50,80.99,'Utilse pour des joutes'),
('Casque Chien',9,1,5,3,'casqueAnimal1.jpg',7,10.99,'Faites parler votre animal intérieur'),
('Casque Chantier',10,2,6,3,'casqueChantier1.jpg',32,15.99,'Pour vous protéger'),
('Casque Contremaitre',10,2,4,3,'casqueChantier2.jpg',25,17.99,'Protège mieux que le casque Chantier'),
('Casque Colonial',8,2,5,3,'casqueColonial.jpg',45,8.99,'Parfait pour explorer l\'Afrique'),
('Casque GIGN',11,2,1,1,'casqueMilitaire1.jpg',37,25.99,'Ne permet pas de devenir agent du GIGN'),
('Casque Soviétique',12,2,2,3,'casqueMilitaire2.jpg',28,18.99,'Parfait pour envahir l\'Afghanistan ou l\'Ukraine'),
('Casque Chat',9,2,7,2,'CasqueMusique1.jpg',48,3.99,'Un casque parfait pour les chat et autres canidés'),
('Casque Wookie',9,2,6,2,'CasqueMusique2.jpg',150,8.99,'Un casque poilant'),
('Casque Musique Pas Fun',9,2,2,2,'CasqueMusique3.jpg',21,4.99,'Un casque sans rien de spécial'),
('Casque de Noel',9,2,3,3,'casqueNoel.jpg',15,31.99,'Avec ce casque, vous pourrez enfin entrer par la cheminé'),
('Casque Pompier',11,2,5,3,'casquePompier.jpg',45,50.99,'Ce casque ne vous permet pas de devenir pompier'),
('Casque Spartiate',8,2,4,1,'casqueSparte1.jpg',28,67.99,'THIS IS SPARTA'),
('Casque Rebelle',13,3,5,4,'CasqueStarWars1.jpeg',78,34.99,'Utile pour les conventions Geek'),
('Casque StormTrooper',13,3,1,4,'CasqueStarWars2.jpeg',55,51.99,'Amélliore votre précision de -99%'),
('Casque Kilo Ren',13,3,2,4,'CasqueStarWars3.jpeg',48,37.99,'Permet de perdre 5 kilos'),
('Casque VR Sony',8,2,2,5,'casqueVR1.jpg',13,105.99,'Un casque VR par Sony'),
('Casque LaserScope',8,2,1,5,'laserScope.jpg',28,98.99,'FIRE FIRE FIRE'),
('Occulus Rift',8,2,2,5,'occulusRift.jpeg',27,352.99,'Un autre casque VR'),
('PediSedate (Game Boy)',8,2,2,5,'pediSedate.jpeg',58,67.99,'Utile pour anesthésier des gens'),
('Passoir Pastafariste',9,2,1,3,'casquePassoir.png',98,48.99,'Casque du parfait adorateur des pâtes'),
('Picole Nationale',9,2,6,3,'casquePicole.png',45,36.99,'Casque officel des forces de l\'ordre'),
('Casque Power Ranger',9,2,3,3,'casquePowerRanger.png',12,53.99,'Ce casque est le ranger Jaune devant, Marron derrière'),
('Casque Romain',6,2,1,1,'casqueRomain.jpeg',68,89.99,'C\'est une antiquité qui vaut cher'),
('Casque Samurai',5,2,1,1,'casqueSamurai.png',78,168.99,'La chute des samurais est proche'),
('Casque Dark Vador',13,2,2,4,'casqueVador.jpg',69,75.99,'Vous allez être trop dark avec ce casque'),
('Casque Ailettes',3,2,1,1,'casqueEpic1.png',35,258.99,'C\'est beau ça...'),
('Casque Garde',3,2,1,1,'casqueSkyrim1.png',48,142.99,'Casque de garde'),
('Casque Sommeil',3,2,1,1,'CasqueSkyrim2.jpeg',39,274.99,'Casque pour dormir tout en se protégant'),
('Casque Ponpon',9,2,5,3,'CasquePonpon.jpg',39,29.99,'Casque avec ponpon'),
('Casque Anglais',1,2,2,3,'casqueAnglais.jpg',29,139.99,'Casque officiel de la garde de la reine'),
('Casque Invisible',8,2,3,3,'casqueInvisible.png',56,896.99,'Vous ne verrez aucune rayures dessus !');