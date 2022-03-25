#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, url_for, flash, session

from connexion_db import get_db

admin_type_casque = Blueprint('admin_type_casque', __name__,
                              template_folder='templates')


@admin_type_casque.route('/admin/type_article/show')
def show_type_article():
    mycursor = get_db().cursor()
    sql = '''select * from type_casque'''
    mycursor.execute(sql)
    typeCasques = mycursor.fetchall()
    return render_template('admin/type_article/show_type_article.html', typeCasques=typeCasques)


@admin_type_casque.route('/admin/type_article/delete/<int:id>', methods=['GET'])
def delete_type_article(id):
    mycursor = get_db().cursor()
    sql = '''select count(id) as countId from modele where type_casque_id=%s'''
    mycursor.execute(sql, id)
    countId = mycursor.fetchone()

    if countId['countId'] > 0:
        flash('il y a des modele possèdant se type de casque : vous ne pouvez pas le supprimer')
    else:
        sql = '''delete from type_casque where id=%s'''
        mycursor.execute(sql, id)
        get_db().commit()
        flash('il y a des modele possèdant se type de casque : vous ne pouvez pas le supprimer')

    return redirect('/admin/type_article/show')


@admin_type_casque.route('/admin/type_article/add')
def add_type_casque():
    return render_template('admin/type_article/add_type_article.html')


@admin_type_casque.route('/admin/type_article/add', methods=['POST'])
def valid_add_type_casque():
    mycursor = get_db().cursor()
    libelle = request.form.get('libelle')
    print("sssssssssssssssssss")
    print(libelle)
    sql = '''insert into type_casque(libelle) value (%s)'''
    mycursor.execute(sql, libelle)
    get_db().commit()

    return redirect('/admin/type_article/show')


@admin_type_casque.route('/admin/type_article/edit/<int:id>', methods=['GET'])
def edit_type_casque(id):
    mycursor = get_db().cursor()
    sql = '''select * from type_casque where id=%s'''
    mycursor.execute(sql, id)
    typeCasque = mycursor.fetchone()
    return render_template('admin/type_article/edit_type_article.html', typeCasque=typeCasque)


@admin_type_casque.route('/admin/type_article/edit', methods=['POST'])
def valid_edit_type_casque():
    mycursor = get_db().cursor()
    libelle = request.form.get('libelle')
    id = request.form.get('id')
    sql = '''update type_casque set libelle=%s where id=%s'''
    mycursor.execute(sql, (libelle, id))
    get_db().commit()

    return redirect('/admin/type_article/show')
