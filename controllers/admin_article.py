#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, url_for, flash, session
from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                          template_folder='templates')


@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    sql = '''select * from modele'''
    mycursor.execute(sql)
    articles = mycursor.fetchall()
    return render_template('admin/article/show_article.html', articles=articles)


@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()

    sql = '''select * from type_casque'''
    mycursor.execute(sql)
    type_casque = mycursor.fetchall()

    sql = '''select * from couleur'''
    mycursor.execute(sql)
    colors = mycursor.fetchall()

    sql = '''select * from fabricant'''
    mycursor.execute(sql)
    fabriquants = mycursor.fetchall()

    sql = '''select * from taille'''
    mycursor.execute(sql)
    tailles = mycursor.fetchall()

    return render_template('admin/article/add_article.html',
                           types_casque=type_casque,
                           couleurs=colors,
                           fabricants=fabriquants,
                           tailles=tailles)


@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_article_id = request.form.get('typeCasque', '')
    prix = request.form.get('prix', '')
    fabricant = request.form.get('fabricant', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')

    if image:
        filename = str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        return redirect(url_for('admin_article.show_article'))

    sql = '''insert into modele(libelle, image, prix, fabricant_id, type_casque_id, description) 
    value (%s,%s,%s,%s,%s,%s)'''

    tupleAdd = (nom, filename, prix, fabricant, type_article_id, description)
    mycursor.execute(sql, tupleAdd)
    get_db().commit()

    print(u'article ajout?? , nom: ', nom, ' - type_article:', type_article_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'article ajout?? , nom:' + nom + '- type_article:' + type_article_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message)
    return redirect(url_for('admin_article.show_article'))


@admin_article.route('/admin/article/delete/<int:id>', methods=['GET'])
def delete_article(id):
    id = str(id)
    mycursor = get_db().cursor()

    sql = '''select count(id) as countC from casque where modele_id=%s'''
    mycursor.execute(sql, id)
    countC = mycursor.fetchone()
    if countC['countC'] > 0:
        flash('il y a des exemplaires dans se mod??le de casque : vous ne pouvez pas le supprimer')
    else:
        sql = '''select image from modele where id=%s'''
        mycursor.execute(sql, id)
        image = mycursor.fetchone()['image']

        sql = '''delete from modele where id=%s'''
        mycursor.execute(sql, id)
        get_db().commit()

        os.remove('static/images/' + image)

        print("un article supprim??, id :", id)
        flash(u'un article supprim??, id : ' + id)

    return redirect(url_for('admin_article.show_article'))


@admin_article.route('/admin/article/edit/<int:id>', methods=['GET'])
def edit_article(id):
    mycursor = get_db().cursor()
    sql = '''select * from modele where id=%s'''
    mycursor.execute(sql, id)
    article = mycursor.fetchall()
    sql = '''select * from type_casque'''
    mycursor.execute(sql)
    types_casques = mycursor.fetchall()
    sql = '''select id, nom from fabricant'''
    mycursor.execute(sql)
    fabricants = mycursor.fetchall()
    sql = '''select * from casque where modele_id=%s'''
    mycursor.execute(sql, id)
    casques = mycursor.fetchall()

    sql = '''select * from taille'''
    mycursor.execute(sql)
    tailles = mycursor.fetchall()

    sql = '''select * from couleur'''
    mycursor.execute(sql)
    couleurs = mycursor.fetchall()

    return render_template('admin/article/edit_article.html', article=article,
                           types_casques=types_casques, fabricants=fabricants,
                           casques=casques, tailles=tailles, couleurs=couleurs)


@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id = request.form.get('id')

    type_casque_id = request.form.get('typeCasque', '')
    prix = request.form.get('prix', '')
    fabricant = request.form.get('fabricant', '')
    image = request.files.get('image')
    description = request.form.get('description')

    mycursor.execute("select image from modele where id=%s", id)
    imageName = mycursor.fetchall()
    imageName = imageName[0]['image']
    if image:
        if imageName != "" and imageName is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", imageName)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", imageName))

        # filename = secure_filename(image.filename)
        image.save(os.path.join('static/images/', imageName))  # filename
        imageName = image.filename

    sql = '''update modele set libelle=%s, image=%s, prix=%s, fabricant_id=%s, type_casque_id=%s, description=%s where id=%s'''


    mycursor.execute(sql, (nom, imageName, prix, fabricant, type_casque_id, description, id))

    get_db().commit()

    message = u'article modifi?? , nom:' + nom + '- type_casque :' + type_casque_id + ' - prix:' + prix + ' - fabricant:' + fabricant + ' - image:' + imageName + ' - description: ' + description
    flash(message)
    return redirect(url_for('admin_article.show_article'))


@admin_article.route('/reboot', methods=['GET'])
def reboot():
    mycursor = get_db().cursor()
    mycursor.execute("update casque set stock=5000")
    get_db().commit()
    flash('Base reboot??e')

    if session["role"] == "ROLE_client":
        return redirect('/client/article/show')
    return redirect('/admin/commande/show')


@admin_article.route('/admin/article/bilan')
def dataviz_article():
    mycursor = get_db().cursor()
    sql = "SELECT type_casque_id,type_casque.libelle as libelle,SUM(prix*stock) as prix_total " \
          "FROM casque " \
          "INNER JOIN modele ON modele.id=casque.modele_id " \
          "INNER JOIN type_casque ON type_casque_id=type_casque.id " \
          "GROUP BY type_casque_id"
    mycursor.execute(sql)
    casques = mycursor.fetchall()
    lPercentage = []
    lLibelle = []
    lTotaux = []

    maxi = 0.0
    for typeCa in casques:
        maxi += float(typeCa["prix_total"])

    for typeC in casques:
        lTotaux.append(float(typeC["prix_total"]))
        if maxi == 0.0:
            lPercentage.append(0.0)
        else:
            lPercentage.append((float(typeC["prix_total"]) / maxi) * 100)
        lLibelle.append(typeC["libelle"])

    mycursor.execute("SELECT type_casque.libelle as libelle, type_casque.id as id, SUM(stock) as stockTotal,"
                     " SUM(stock*prix) as coutTotal "
                     "FROM type_casque "
                     "LEFT JOIN modele ON modele.type_casque_id=type_casque.id "
                     "LEFT JOIN casque on casque.modele_id=modele.id "
                     "GROUP BY type_casque.id")
    tableau = mycursor.fetchall()

    sql = "select substring(code,1,2) as dep, count(substring(code,1,2)) as nombre " \
          "from adresse " \
          "group by substring(code,1,2)"
    mycursor.execute(sql)
    adresse = mycursor.fetchall()
    maxAddress = 0
    for element in adresse:
        if element['nombre'] > maxAddress:
            maxAddress = element['nombre']

    lettre = "FEDCBA9876543210"
    couleur = ['#' + lettre[int(i / maxAddress * 16) - 1] * 6 for i in range(maxAddress + 1)]
    print(couleur)

    return render_template('admin/dataviz/etat_article_vente.html', tableau=tableau, casques=casques,
                           percentages=lPercentage, libelle=lLibelle, totaux=lTotaux,
                           adresse=adresse, couleur=couleur)


@admin_article.route('/admin/article/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()

    mycursor.execute("SELECT * FROM modele where id = %s", id)
    article = mycursor.fetchone()

    mycursor.execute("SELECT * FROM avis where casque_id = %s", id)
    commentaires = mycursor.fetchall()

    return render_template('admin/article/show_avis.html', article=article, commentaires=commentaires)


@admin_article.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    userId = request.form.get('idUser', None)
    malus = request.form.get('malus', None)
    mycursor.execute("DELETE FROM avis WHERE casque_id=%s AND user_id=%s", (article_id, userId))
    if malus is not None:
        mycursor.execute("INSERT INTO coupons (valeur,user_id) VALUES (%s,%s)", (-50, userId))
    get_db().commit()

    return admin_avis(article_id)
