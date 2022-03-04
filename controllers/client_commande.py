#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, flash, session
from connexion_db import get_db,update_property
import random

client_commande = Blueprint('client_commande', __name__,
                            template_folder='templates')


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    user_id = session['user_id']
    sql = "select * " \
          "from panier " \
          "INNER JOIN casque ON casque.id=panier.casque_id " \
          "INNER JOIN modele ON modele.id=casque.modele_id "\
            "where user_id=%s"
    mycursor.execute(sql, user_id)
    totPanier = mycursor.fetchall()

    idCoupon = request.form.get("coupon_id",None)
    typeLivraison = request.form.get("type_id",None)
    adresse_factu = request.form.get("adresse_fac", None)
    adresse_livraison = request.form.get("adresse_livraison", None)

    valCoupon = 0
    if not idCoupon in ("IGNORE",None):
        mycursor.execute("SELECT * FROM coupons WHERE id = %s",idCoupon)
        valCoupon = int(mycursor.fetchone()["valeur"])
        mycursor.execute("DELETE FROM coupons WHERE id = %s",idCoupon)
        get_db().commit()


    # cree une ligne commande pour l'utilisateur
    sql = "insert into commande values (null,CURDATE(),%s,1,%s,%s,%s,%s,%s)"
    mycursor.execute(sql, (user_id,typeLivraison,adresse_livraison,adresse_factu,session['clic'],valCoupon))
    get_db().commit()

    # recupere id commande
    id = mycursor.lastrowid

    mycursor.execute("select * from type_livraison where id=%s",(typeLivraison))
    tLivraison = mycursor.fetchone()

    sql = "insert into ligne_commande values (%s,%s,%s,%s)"
    sql2 = "select * from casque where id=%s"
    sql3 = "update casque set stock=%s where id=%s"
    cout_tot = 0
    for ligne in totPanier:
        # passe du panier a ligne_commande
        tuple = (id, ligne['casque_id'], ligne['prix'], ligne['quantite'])
        mycursor.execute(sql, tuple)

        # recupere etat du stock et soustrait la quantite achetee
        mycursor.execute(sql2, (ligne['casque_id']))
        quantite = mycursor.fetchone()['stock'] - int(ligne['quantite'])
        cout_tot += float(ligne['quantite']) * float(ligne['prix'])
        mycursor.execute(sql3, (quantite, ligne['casque_id']))

    # efface panier du client
    sql = "delete from panier where user_id=%s"
    mycursor.execute(sql, user_id)

    # envoie mail
    mycursor.execute(
        "INSERT INTO mails(owner_id,sender_id,receiver_id,objetMail,texteMail,dateEnvoi) VALUES (%s,%s,%s,%s,%s,CURDATE())",
        (user_id,1, user_id, "Commande n°"+str(id), "Bonjour, votre commande est en cours de validation."))

    # reduit solde

    update_property("solde",-((cout_tot * float(tLivraison["valeurAjoute"])+session["clic"])*(100-valCoupon)/100))

    # ajout d'un coupons toute les 5 commandes
    mycursor.execute("SELECT * FROM commande WHERE user_id = %s",(user_id))
    if len(mycursor.fetchall()) % 5 == 0:
        # Ajout d'un coupon
        mycursor.execute("INSERT INTO coupons(valeur,user_id) VALUES (%s,%s)",(random.randint(1,20),user_id))

    get_db().commit()
    flash(u'Commande ajoutée')
    return redirect('/client/article/show')


@client_commande.route('/client/commande/show', methods=['GET', 'POST'])
def client_commande_show():
    mycursor = get_db().cursor()

    currentCommande = request.form.get("idCommande", '')

    sql = "select commande.id,etat.libelle,date_achat,etat_id," \
                "count(*) as nbr_articles," \
                "sum(quantite) as nb_tot," \
                "(sum(prix_unit*quantite)*valeurAjoute+clic)*(100-reduction)/100 as prix_total," \
                "adresse.ville as ville " \
          "from commande " \
          "inner join ligne_commande on commande.id=ligne_commande.commande_id " \
          "inner join etat on commande.etat_id=etat.id " \
          "inner join type_livraison on type_livraison.id=type_livraison_id " \
          "left join adresse on adresse.id=commande.adresse_id_livraison " \
          "where commande.user_id=%s " \
          "group by commande.id"
    mycursor.execute(sql, session['user_id'])
    commandes = mycursor.fetchall()

    if currentCommande is not None:
        sql = "SELECT quantite,prix_unit as prix,modele.libelle as nom,sum(prix_unit*quantite) as prix_ligne,couleur.libelle as cl, taille.libelle as tl " \
              "FROM ligne_commande " \
              "INNER JOIN casque ON casque_id = casque.id " \
              "INNER JOIN modele ON modele.id=casque.modele_id " \
              "INNER JOIN couleur ON couleur.id=casque.couleur_id "\
            "INNER JOIN taille ON taille.id=casque.taille_id  "\
              "WHERE commande_id = %s " \
              "GROUP BY casque.id"
        mycursor.execute(sql, currentCommande)
        articles_commande = mycursor.fetchall()

        sql="SELECT libelle,valeurAjoute,clic,reduction, " \
                "sum(prix_unit*quantite)*(valeurAjoute-1) AS supplement, " \
                "(sum(prix_unit*quantite)*valeurAjoute+clic)*(100-reduction)/100 AS total, " \
                "al.ville, al.code, al.rue,al.numero , af.ville,af.code ,af.rue,af.numero " \
            "FROM type_livraison " \
            "INNER JOIN commande ON type_livraison_id=type_livraison.id " \
            "INNER JOIN ligne_commande ON commande.id=ligne_commande.commande_id "\
            "INNER JOIN adresse AS al ON adresse_id_livraison=al.id " \
            "INNER JOIN adresse AS af ON adresse_id_facturation=af.id " \
            "WHERE commande.id = %s"
        mycursor.execute(sql, currentCommande)
        suplement = mycursor.fetchone()
        print(suplement)
    else:
        articles_commande = None

    if 'clic' in session:
        session['clic'] += 1
    return render_template('client/commandes/show.html', commandes=commandes, articles_commande=articles_commande, commande_id=currentCommande,suplementL=suplement)
