-- drop
drop table if exists Ligne;
drop table if exists Commande;
drop table if exists Client;
drop table if exists Article;

-- create
create table if not exists Article(
    idArticle int auto_increment,
    designation varchar(50),
    prix numeric(5,2),

    primary key (idArticle)
)character set 'utf8';

create table if not exists Client(
    idClient int auto_increment,
    nom varchar(50),
    ville varchar(50),

    primary key (idClient)
)character set 'utf8';

create table if not exists Commande(
    idCommande int auto_increment,
    dateCommande date,
    idClient int,

    primary key (idCommande),
    constraint fk_commande_client
        foreign key (idClient) references Client(idClient)
)character set 'utf8';

create table if not exists Ligne(
    idCommande int,
    idArticle int,
    quantite int,

    primary key (idCommande,idArticle),
    constraint fk_ligne_commande
        foreign key (idCommande) references Commande(idCommande),
    constraint fk_ligne_article
        foreign key (idArticle) references Article(idArticle)
)character set 'utf8';

-- insert / load
LOAD DATA LOCAL INFILE 'data/Article.csv' INTO TABLE Article CHARACTER SET utf8
FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'data/Client.csv' INTO TABLE Client CHARACTER SET utf8
FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'data/Commande.csv' INTO TABLE Commande CHARACTER SET utf8
FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'data/Ligne.csv' INTO TABLE Ligne CHARACTER SET utf8
FIELDS TERMINATED BY ',';

alter table Commande drop foreign key fk_commande_client;
alter table Ligne drop foreign key fk_ligne_article;
alter table Ligne drop foreign key fk_ligne_commande;

alter table Commande
    add constraint fk_commande_client
        foreign key (idClient) references Client(idClient) on delete cascade;
alter table Ligne
    add constraint fk_ligne_commande
        foreign key (idCommande) references Commande(idCommande) on delete cascade;
alter table Ligne
    add constraint fk_ligne_article
        foreign key (idArticle) references Article(idArticle) on delete cascade;

show create table Commande;
show create table Ligne;

delete from Client where nom like 'Mutz';
select * from Client;
select * from Commande;

-- r1
select nom
from Client
where ville='Belfort'
  and (nom like 'm%' or nom like 'e%' or nom like 'd%')
order by nom;

-- r2
select designation,prix
from Article
where prix>=6 and prix<=10 and designation like '%lég%'
order by designation;

-- r3
select nom,dateCommande
from Client
inner join Commande C on Client.idClient = C.idClient
where nom like '%Mutz%';

-- r4
select nom,designation,prix,quantite,Commande.idCommande
from Article
inner join Ligne on Article.idArticle = Ligne.idArticle
inner join Commande on Ligne.idCommande = Commande.idCommande
inner join Client on Commande.idClient = Client.idClient
where nom like '%Mutz%';

-- r5
select nom,designation,Commande.idCommande,prix*quantite as ca
from Article
inner join Ligne on Article.idArticle = Ligne.idArticle
inner join Commande on Ligne.idCommande = Commande.idCommande
inner join Client on Commande.idClient = Client.idClient
where nom like '%Mutz%'
order by ca desc;

-- r6
select nom,Commande.idCommande,SUM(prix*quantite) as prix_total
from Article
inner join Ligne on Article.idArticle = Ligne.idArticle
inner join Commande on Ligne.idCommande = Commande.idCommande
inner join Client on Commande.idClient = Client.idClient
where nom='Mutz'
group by Commande.idCommande, nom;


-- r7
select nom,Commande.idCommande,SUM(prix*quantite) as prix_total,
       SUM(prix*quantite)/5 as TVA, SUM(prix*quantite)*1.2 as prix_total_TTC
from Article
inner join Ligne on Article.idArticle = Ligne.idArticle
inner join Commande on Ligne.idCommande = Commande.idCommande
inner join Client on Commande.idClient = Client.idClient
group by Commande.idCommande, nom
order by SUM(prix*quantite);

-- r8
select designation,quantite as QteCommande,year(dateCommande),Commande.idCommande
from Article
left join  Ligne on Ligne.idArticle = Article.idArticle
left join Commande on Ligne.idCommande = Commande.idCommande
order by designation;