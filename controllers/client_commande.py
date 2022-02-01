#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    user_id=session['user_id']
    sql="select * from panier INNER JOIN casque ON casque.id=panier.casque_id where user_id=%s"
    mycursor.execute(sql, (user_id))
    totPanier=mycursor.fetchall()

    # cree une ligne commande pour l'utilisateur
    sql = "insert into commande values (null,CURDATE(),%s,1)"
    mycursor.execute(sql, (user_id))
    get_db().commit()
    id = mycursor.lastrowid #recupere id commande
    # = '''select last_insert_id()'''

    sql="insert into ligne_commande values (%s,%s,%s,%s)"
    sql2 = "select * from casque where id=%s"
    sql3="update casque set stock=%s where id=%s"
    for ligne in totPanier:
        # passe du panier a ligne_commande
        tuple=(id,ligne['casque_id'],ligne['prix'],ligne['quantite'])
        mycursor.execute(sql,tuple)

        # recupere etat du stock et soustrait la quantite achetee
        mycursor.execute(sql2,(ligne['casque_id']))
        quantite = mycursor.fetchone()['stock']-int(ligne['quantite'])
        mycursor.execute(sql3, (quantite,ligne['casque_id']))

    #efface panier du client
    sql="delete from panier where user_id=%s"
    mycursor.execute(sql, (user_id))
    get_db().commit()

    flash(u'Commande ajoutée')
    return redirect('/client/article/show')



@client_commande.route('/client/commande/show', methods=['GET','POST'])
def client_commande_show():
    mycursor = get_db().cursor()

    currentCommande = request.form.get("idCommande",'')
    print("commande : ",currentCommande)

    sql = "select commande.id,libelle,date_achat, count(*) as nbr_articles,sum(quantite) as nb_tot,sum(prix_unit*quantite) as prix_total,etat_id " \
        "from commande " \
        "inner join ligne_commande on commande.id=ligne_commande.commande_id " \
        "inner join etat on commande.etat_id=etat.id" \
          " where user_id=%s " \
          "group by commande.id,date_achat,etat_id;"
    mycursor.execute(sql,session['user_id'])
    commandes = mycursor.fetchall()

    if currentCommande is not None:
        sql = "SELECT quantite,prix_unit as prix,casque.libelle as nom,sum(prix_unit*quantite) as prix_ligne " \
              "FROM ligne_commande " \
              "INNER JOIN casque ON casque_id = casque.id " \
              "WHERE commande_id = %s " \
              "GROUP BY casque.id"
        mycursor.execute(sql,(currentCommande))
        articles_commande = mycursor.fetchall()
    else:
        articles_commande = None
    return render_template('client/commandes/show.html', commandes=commandes, articles_commande=articles_commande)

