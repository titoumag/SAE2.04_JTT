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
    sql="select * from panier where user_id=%s"
    mycursor.execute(sql, (user_id))
    totPanier=mycursor.fetchall()

    # cree une ligne commande pour l'utilisateur
    sql = "insert into commande values (null,CURDATE(),%s,1)"
    mycursor.execute(sql, (user_id))
    get_db().commit()
    id = mycursor.lastrowid #recupere id commande

    sql="insert into ligne_commande values (%s,%s,%s,%s)"
    sql2 = "select * from casque where id=%s"
    sql3="update casque set stock=%s where id=%s"
    for ligne in totPanier:
        # passe du panier a ligne_commande
        tuple=(id,ligne['casque_id'],ligne['prix_unit'],ligne['quantite'])
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



@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    commandes = None
    articles_commande = None
    return render_template('client/commandes/show.html', commandes=commandes, articles_commande=articles_commande)

