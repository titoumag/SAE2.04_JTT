#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')      # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()

    debut = True
    params = []
    sql = "SELECT * FROM casque"
    if "filter_word" in session.keys():
        sql+=" WHERE libelle LIKE %s"
        params.append("%"+session['filter_word']+"%")
        debut = False
    if "filter_types" in session.keys() and len(session['filter_types'])>0:
        if len(session['filter_types']) == 1: tpl = "('" + str(session['filter_types'][0]) + "')"
        else: tpl = str(tuple(session['filter_types']))
        if debut: sql+=" WHERE type_casque_id in "+tpl
        else: sql+=" AND type_casque_id in "+tpl
        debut=False
    if "filter_prix_min" in session.keys() !="":
        if debut: sql+=" WHERE prix > %s"
        else: sql+=" AND prix > %s"
        debut=False
        params.append(session['filter_prix_min'])
    if "filter_prix_max" in session.keys() !="":
        if debut: sql+=" WHERE prix < %s"
        else: sql+=" AND prix < %s"
        params.append(session['filter_prix_max'])

    mycursor.execute(sql,params)
    articles = mycursor.fetchall()



    mycursor.execute("SELECT * FROM type_casque")
    types_articles = mycursor.fetchall()
    articles_panier = []
    prix_total = None
    return render_template('client/boutique/panier_article.html', articles=articles, articlesPanier=articles_panier, prix_total=prix_total, itemsFiltre=types_articles)

@client_article.route('/client/article/details/<int:id>', methods=['GET'])
def client_article_details(id):
    mycursor = get_db().cursor()
    article=None
    commentaires=None
    commandes_articles=None
    return render_template('client/boutique/article_details.html', article=article, commentaires=commentaires, commandes_articles=commandes_articles)