#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')

# NOUVELLE FONCTION : ajoute et enleve a la quantite du panier
@client_panier.route('/client/panier/update',methods=['POST'])
def client_panier_update():
    mycursor = get_db().cursor()
    idArticle = request.form.get('idArticle')
    direction = int(request.form.get('quantite'))
    user_id = session['user_id']

    sql = "select * from panier where casque_id=%s and user_id=%s"
    mycursor.execute(sql, (idArticle,user_id))
    res = mycursor.fetchall()

    if len(res) == 0:
        sql = "select prix from casque where id=%s"
        mycursor.execute(sql, (idArticle))
        prix = mycursor.fetchone()['prix']

        sql="insert into panier value (null,CURDATE(),%s,%s,%s,%s)"
        tuple=(prix,direction,idArticle,user_id)
        mycursor.execute(sql, tuple)
        get_db().commit()

    else:
        quantite = int(res[0]['quantite']) + direction
        sql = "select * from casque where id=%s"
        mycursor.execute(sql, (idArticle))
        stock = int(mycursor.fetchone()['stock'])

        if (direction==-1 and quantite>0) or (direction==1 and quantite<stock+1):
            sql="update panier set quantite=%s where casque_id=%s and user_id=%s "
            mycursor.execute(sql, (quantite,idArticle, user_id))
            get_db().commit()

    return redirect('/client/article/show')

@client_panier.route('/client/panier/all', methods=['POST'])
def client_panier_all():
    mycursor = get_db().cursor()
    user_id = session['user_id']

    sql = "select * from casque"
    mycursor.execute(sql)
    totStock = mycursor.fetchall()

    sql="insert into panier value (null,CURDATE(),%s,%s,%s,%s)"
    for article in totStock:
        tuple=(article['prix'],article['stock'],article['id'],user_id)
        mycursor.execute(sql, tuple)
    get_db().commit()

    return redirect('/client/article/show')


# ANCIENNE FONCTION PLUS UTILISEE : replacée par update()
@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    return redirect('/client/panier/update')
# ANCIENNE FONCTION PLUS UTILISEE : replacée par update()
@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    user_id = session['user_id']

    sql = 'DELETE FROM panier WHERE user_id=%s'
    tuple = (user_id)
    mycursor.execute(sql, tuple)
    get_db().commit()

    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    idArticle = request.form.get('idArticle')
    user_id = session['user_id']
    print(idArticle,user_id)

    sql = 'DELETE FROM panier WHERE user_id=%s and casque_id=%s'
    tuple = (user_id, idArticle)
    mycursor.execute(sql, tuple)
    get_db().commit()


    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    # SQL
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    if type(filter_word) == str:
        session['filter_word'] = filter_word
    session['filter_prix_min'] = filter_prix_min
    session['filter_prix_max'] = filter_prix_max
    session['filter_types'] = filter_types
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    print("suppr filtre")
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))
