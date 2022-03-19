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
    sql = "SELECT modele.id,libelle,description,image,sum(stock) as stock,prix,fabricant_id,type_casque_id," \
          "count(avis.user_id) as nb_avis,AVG(avis.note) as moy_notes " \
          "FROM modele " \
          "INNER JOIN casque ON casque.modele_id=modele.id " \
          "LEFT JOIN avis ON casque.id = avis.casque_id "
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

    sql += " GROUP BY modele.id"
    mycursor.execute(sql, params)
    articles = mycursor.fetchall()

    mycursor.execute("SELECT * FROM type_casque")
    types_articles = mycursor.fetchall()

    mycursor.execute("SELECT * "
                     "FROM panier "
                     "INNER JOIN casque ON panier.casque_id=casque.id "
                     "INNER JOIN modele ON modele.id=casque.modele_id "
                     "INNER JOIN couleur ON couleur.id=casque.couleur_id "
                     "INNER JOIN taille ON taille.id=casque.taille_id  "
                     "WHERE user_id=%s",
                     session['user_id'])
    articles_panier = mycursor.fetchall()
    print(articles_panier)

    sql = "select sum(quantite*prix) as prix_tot " \
          "FROM panier " \
          "INNER JOIN casque on casque.id=panier.casque_id " \
          "INNER JOIN modele ON modele.id=casque.modele_id " \
          "WHERE user_id=%s"
    mycursor.execute(sql, session['user_id'])
    prix_total = mycursor.fetchone()['prix_tot']

    mycursor.execute("select * from user where id=%s", session['user_id'])
    user = mycursor.fetchone()

    mycursor.execute("SELECT * FROM type_livraison")
    type_livraison = mycursor.fetchall()

    mycursor.execute("SELECT * FROM adresse WHERE user_id=%s", session['user_id'])
    adresse = mycursor.fetchall()

    mycursor.execute("SELECT * FROM coupons WHERE user_id=%s", session["user_id"])
    coupons = mycursor.fetchall()

    if 'clic' in session:
        session['clic'] += 1
    return render_template('client/boutique/panier_article.html', articles=articles, articlesPanier=articles_panier,
                           prix_total=prix_total, itemsFiltre=types_articles, user=user, type_livraison=type_livraison,
                           clic=session['clic'], liste_adresse=adresse, coupons=coupons)


@client_article.route('/client/article/details/<int:id>', methods=['GET'])
def client_article_details(id):
    mycursor = get_db().cursor()

    mycursor.execute("SELECT * FROM modele where id = %s", id)
    article = mycursor.fetchone()

    mycursor.execute("SELECT * "
                     "FROM casque "
                     "INNER JOIN couleur ON couleur.id=casque.couleur_id "
                     "INNER JOIN taille ON taille.id=casque.taille_id  "
                     "where modele_id = %s and stock>0 and casque.id in ("
                     "select casque.id "
                     "from casque "
                     "left join panier on panier.casque_id=casque.id "
                     "where stock>quantite or quantite is null)", id)
    choix = mycursor.fetchall()

    mycursor.execute("SELECT * FROM avis where casque_id = %s", id)
    commentaires = mycursor.fetchall()

    mycursor.execute(
        "SELECT * FROM ligne_commande INNER JOIN commande ON ligne_commande.commande_id = commande.id WHERE casque_id = %s AND user_id = %s",
        (id, session["user_id"]))
    commandes_articles = mycursor.fetchall()

    mycursor.execute("SELECT * FROM avis WHERE casque_id = %s AND user_id = %s", (id, session["user_id"]))
    userHasMadeAComment = mycursor.fetchall() != ()

    print(choix)

    if 'clic' in session:
        session['clic'] += 1
    return render_template('client/boutique/article_details.html', article=article, commentaires=commentaires,
                           commandes_articles=commandes_articles, userHasMadeAComment=userHasMadeAComment,
                           choix=choix)
