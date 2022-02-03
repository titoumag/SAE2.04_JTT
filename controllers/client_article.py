#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import render_template, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                           template_folder='templates')


@client_article.route('/client/index')
@client_article.route('/client/article/show')  # remplace /client
def client_article_show():  # remplace client_index
    mycursor = get_db().cursor()

    debut = True
    params = []
    sql = "SELECT id,libelle,image,stock,prix,fabricant_id,taille_id,couleur_id,type_casque_id,count(avis.user_id) as nb_avis,AVG(avis.note) as moy_notes " \
          "FROM casque LEFT JOIN avis ON casque.id = avis.casque_id"
    if "filter_word" in session.keys():
        sql += " WHERE libelle LIKE %s"
        params.append("%" + session['filter_word'] + "%")
        debut = False
    if "filter_types" in session.keys() and len(session['filter_types']) > 0:
        if len(session['filter_types']) == 1:
            tpl = "('" + str(session['filter_types'][0]) + "')"
        else:
            tpl = str(tuple(session['filter_types']))
        if debut:
            sql += " WHERE type_casque_id in " + tpl
        else:
            sql += " AND type_casque_id in " + tpl
        debut = False
    if "filter_prix_min" in session.keys() and session["filter_prix_min"] != "":
        if debut:
            sql += " WHERE prix > %s"
        else:
            sql += " AND prix > %s"
        debut = False
        params.append(session['filter_prix_min'])
    if "filter_prix_max" in session.keys() and session["filter_prix_max"] != "":
        if debut:
            sql += " WHERE prix < %s"
        else:
            sql += " AND prix < %s"
        params.append(session['filter_prix_max'])

    sql+= " GROUP BY id"
    mycursor.execute(sql, params)
    articles = mycursor.fetchall()

    mycursor.execute("SELECT * FROM type_casque")
    types_articles = mycursor.fetchall()

    mycursor.execute("SELECT * FROM panier INNER JOIN casque ON panier.casque_id=casque.id WHERE user_id=%s",
                     session['user_id'])
    articles_panier = mycursor.fetchall()

    sql="select sum(quantite*prix) as prix_tot " \
        "FROM panier " \
        "INNER JOIN casque on casque.id=panier.casque_id " \
        "WHERE user_id=%s"
    mycursor.execute(sql, session['user_id'])
    prix_total = mycursor.fetchone()['prix_tot']

    mycursor.execute("select * from user where id=%s", session['user_id'])
    user=mycursor.fetchone()


    return render_template('client/boutique/panier_article.html', articles=articles, articlesPanier=articles_panier,
                           prix_total=prix_total, itemsFiltre=types_articles,user=user)


@client_article.route('/client/article/details/<int:id>', methods=['GET'])
def client_article_details(id):
    mycursor = get_db().cursor()

    mycursor.execute("SELECT * FROM casque where id = %s",(id))
    article = mycursor.fetchone()

    mycursor.execute("SELECT * FROM avis where casque_id = %s", (id))
    commentaires = mycursor.fetchall()

    mycursor.execute("SELECT * FROM ligne_commande INNER JOIN commande ON ligne_commande.commande_id = commande.id WHERE casque_id = %s AND user_id = %s", (id,session["user_id"]))
    commandes_articles = mycursor.fetchall()


    mycursor.execute("SELECT * FROM avis WHERE casque_id = %s AND user_id = %s",(id,session["user_id"]))
    userHasMadeAComment = mycursor.fetchall() != ()

    return render_template('client/boutique/article_details.html', article=article, commentaires=commentaires,
                           commandes_articles=commandes_articles,userHasMadeAComment=userHasMadeAComment)
