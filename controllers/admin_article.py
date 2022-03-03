#! /usr/bin/python
# -*- coding:utf-8 -*-
import os.path

from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                          template_folder='templates')


@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    sql = '''select * from casque'''
    mycursor.execute(sql)
    articles = mycursor.fetchall()
    # print(articles)
    return render_template('admin/article/show_article.html', articles=articles)


@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()
    types_articles = None
    return render_template('admin/article/add_article.html', types_articles=types_articles)


@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    nom = request.form.get('nom', '')
    type_article_id = request.form.get('type_article_id', '')
    # type_article_id = int(type_article_id)
    prix = request.form.get('prix', '')
    stock = request.form.get('stock', '')
    description = request.form.get('description', '')
    image = request.form.get('image', '')

    print(u'article ajouté , nom: ', nom, ' - type_article:', type_article_id, ' - prix:', prix, ' - stock:', stock,
          ' - description:', description, ' - image:', image)
    message = u'article ajouté , nom:' + nom + '- type_article:' + type_article_id + ' - prix:' + prix + ' - stock:' + stock + ' - description:' + description + ' - image:' + image
    flash(message)
    return redirect(url_for('admin_article.show_article'))


@admin_article.route('/admin/article/delete', methods=['POST'])
def delete_article():
    # id = request.args.get('id', '')
    id = request.form.get('id', '')

    print("un article supprimé, id :", id)
    flash(u'un article supprimé, id : ' + id)
    return redirect(url_for('admin_article.show_article'))


@admin_article.route('/admin/article/edit/<int:id>', methods=['GET'])
def edit_article(id):
    mycursor = get_db().cursor()
    sql = '''select * from casque where id=%s'''
    mycursor.execute(sql, id)
    article = mycursor.fetchall()
    sql = '''select * from type_casque'''
    mycursor.execute(sql)
    types_casques = mycursor.fetchall()
    sql = '''select id, nom from fabricant'''
    mycursor.execute(sql)
    fabricants = mycursor.fetchall()
    sql = '''select * from couleur'''
    mycursor.execute(sql)
    couleurs = mycursor.fetchall()
    print(article)
    return render_template('admin/article/edit_article.html', article=article,
                           types_casques=types_casques, fabricants=fabricants,
                           couleurs=couleurs)


@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    nom = request.form['nom']
    id = request.form.get('id', '')
    type_casque_id = request.form.get('type_casque_id', '')
    prix = request.form.get('prix', '')
    stock = request.form.get('stock', '')
    fabricant = request.form.get('fabricant', '')
    image = request.files.get('image')
    filename = secure_filename(image.filename)
    image.save(os.path.join('static/images/', filename))
    couleur = request.form.get('couleur', '')
    # sql = '''update casque set libelle=%s, image=%s, stock=%s, prix=%s, couleur_id=%s, fabricant_id=%s, type_casque_id=%s  where id=%s'''
    # print(sql)

    print(nom, image, stock, prix, couleur, fabricant, type_casque_id, id)
    # mycursor.execute(sql, (nom, image, stock,
    #                        prix, couleur, fabricant,
    #                        type_casque_id, id))

    # get_db().commit()

    print(u'article modifié , nom : ', nom, ' - type_casque :', type_casque_id, ' - prix:', prix, ' - stock:', stock,
          ' - fabricant:', fabricant, ' - image:', image)
    message = u'article modifié , nom:' + nom + '- type_casque :' + type_casque_id + ' - prix:' + prix + ' - stock:' + stock + ' - fabricant:' + fabricant + ' - image:' + image
    flash(message)
    return redirect(url_for('admin_article.show_article'))


@admin_article.route('/reboot', methods=['GET'])
def reboot():
    mycursor = get_db().cursor()
    mycursor.execute("update casque set stock=5000")
    get_db().commit()
    flash('Base rebootée')

    if session["role"] == "ROLE_client":
        return redirect('/client/article/show')
    return redirect('/admin/commande/show')


@admin_article.route('/admin/article/bilan')
def dataviz_article():
    mycursor = get_db().cursor()
    sql = "SELECT type_casque_id,type_casque.libelle as libelle,SUM(prix*stock) as prix_total " \
          "FROM casque " \
          "INNER JOIN type_casque ON type_casque_id=type_casque.id " \
          "GROUP BY type_casque_id"
    mycursor.execute(sql)
    casques = mycursor.fetchall()
    lPercentage = []
    lLibelle = []
    lTotaux = []

    maxi = 0.0
    for type in casques:
        maxi += float(type["prix_total"])

    for type in casques:
        lTotaux.append(float(type["prix_total"]))
        if maxi == 0.0:
            lPercentage.append(0.0)
        else:
            lPercentage.append((float(type["prix_total"]) / maxi) * 100)
        lLibelle.append(type["libelle"])

    mycursor.execute("SELECT type_casque.libelle as libelle, type_casque.id as id, SUM(stock) as stockTotal,"
                     " SUM(stock*prix) as coutTotal "
                     "FROM type_casque "
                     "LEFT JOIN casque on casque.type_casque_id=type_casque.id "
                     "GROUP BY type_casque.id")
    tableau = mycursor.fetchall()

    sql = "select substring(code,1,2) as dep, count(substring(code,1,2)) as nombre " \
          "from adresse " \
          "group by substring(code,1,2)"
    mycursor.execute(sql)
    adresse = mycursor.fetchall()
    max = 0
    for element in adresse:
        if element['nombre'] > max:
            max = element['nombre']

    lettre = "FEDCBA9876543210"
    couleur = ['#' + lettre[int(i / max * 16) - 1] * 6 for i in range(1, max + 1)]
    print(couleur)

    return render_template('admin/dataviz/etat_article_vente.html', tableau=tableau, casques=casques,
                           percentages=lPercentage, libelle=lLibelle, totaux=lTotaux,
                           adresse=adresse, couleur=couleur)
