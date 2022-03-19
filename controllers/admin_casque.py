#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, url_for, flash

from connexion_db import get_db

admin_casque = Blueprint('admin_casque', __name__,
                         template_folder='templates')


@admin_casque.route('/admin/article/casque/<int:id>/add')
def add_casque(id):
    mycursor = get_db().cursor()

    sql = '''select id, image from modele where id=%s'''
    mycursor.execute(sql, id)
    article = mycursor.fetchall()[0]

    sql = '''select * from couleur'''
    mycursor.execute(sql)
    couleurs = mycursor.fetchall()

    sql = '''select * from taille'''
    mycursor.execute(sql)
    tailles = mycursor.fetchall()

    return render_template('admin/article/casque/add_casque.html', article=article, couleurs=couleurs, tailles=tailles)


@admin_casque.route('/admin/article/casque/add', methods=['POST'])
def valid_add_casque():
    mycursor = get_db().cursor()

    id_modele = request.form.get('id')
    stock = request.form.get('stock')
    taille = request.form.get('taille')
    print(taille)
    couleur = request.form.get('couleur')
    print(couleur)

    sql = '''insert into casque(modele_id, stock, taille_id, couleur_id)
    value (%s,%s,%s,%s)'''

    tupleAdd = (id_modele, stock, taille, couleur)
    mycursor.execute(sql, tupleAdd)
    get_db().commit()

    message = u'casque ajouté , modele_id:' + id_modele + '- stock:' + stock + ' - couleur:' + couleur + ' - taille:' + taille
    flash(message)
    return redirect('/admin/article/edit/' + id_modele)


@admin_casque.route('/admin/article/casque/edit/<int:id>', methods=['GET'])
def edit_casque(id):
    mycursor = get_db().cursor()
    sql = '''select * from taille'''
    mycursor.execute(sql)
    tailles = mycursor.fetchall()
    sql = '''select * from couleur'''
    mycursor.execute(sql)
    couleurs = mycursor.fetchall()
    sql = '''select * from casque where id=%s'''
    mycursor.execute(sql, id)
    casque = mycursor.fetchall()[0]

    sql = '''select libelle, image from modele where id=%s'''
    mycursor.execute(sql, int(casque['modele_id']))
    article = mycursor.fetchall()[0]
    print(casque)
    return render_template('admin/article/casque/edit_casque.html', tailles=tailles, couleurs=couleurs, casque=casque, article=article)


@admin_casque.route('/admin/article/casque/edit', methods=['POST'])
def valid_edit_casque():
    id = request.form.get('id')
    idModele = request.form.get('idModele')
    stock = request.form.get('stock')
    taille_id = request.form.get('idTaille')
    couleur_id = request.form.get('idCouleur')

    mycursor = get_db().cursor()
    sql = '''update casque set stock=%s, taille_id=%s, couleur_id=%s where id=%s'''
    mycursor.execute(sql, (stock, taille_id, couleur_id, id))
    get_db().commit()

    message = u'casque modifié , id:' + str(id) + '- stock :' + str(stock) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id)
    flash(message)

    return redirect('/admin/article/edit/' + str(idModele))


@admin_casque.route('/admin/article/casque/delete/<int:idDel>.<int:idArt>', methods=['GET'])
def admin_delete_exemplaires(idDel, idArt):
    sql = '''delete from casque where id=%s'''
    mycursor = get_db().cursor()
    mycursor.execute(sql, idDel)
    get_db().commit()

    print("un exemplaire supprimé, id :", idDel)
    flash(u'un exemplaire supprimé, id : ' + str(idDel))

    return redirect('/admin/article/edit/' + str(idArt))
