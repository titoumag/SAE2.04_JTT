#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import render_template, redirect
from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                           template_folder='templates')


@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get', 'post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    sql = "SELECT id, user_id, SUM(quantite) as commande_quantite,SUM(quantite*prix_unit) as prix_tot, etat_id, date_achat " \
          "FROM ligne_commande " \
          "INNER JOIN commande on commande.id=ligne_commande.commande_id " \
          "GROUP BY commande.id"
    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    return render_template('admin/commandes/show.html', commandes=commandes)


@admin_commande.route('/admin/commande/valider/<int:id>', methods=['get', 'post'])
def admin_commande_valider(id):
    mycursor = get_db().cursor()
    sql = '''UPDATE commande SET etat_id=2 WHERE commande.id=%s'''
    mycursor.execute(sql, id)
    get_db().commit()
    return redirect('/admin/commande/show')


@admin_commande.route('/admin/commande/<int:id>', methods=['get', 'post'])
def admin_commande_details(id):
    mycursor = get_db().cursor()
    sql = '''select commande_id, casque.libelle as libelle, prix_unit, quantite, prix_unit*quantite as prix_tot from
     ligne_commande INNER JOIN casque on casque.id = casque_id where commande_id = %s'''
    mycursor.execute(sql, id)
    articles = mycursor.fetchall()
    sql = '''select libelle from etat inner join commande on commande.etat_id=etat.id where commande.id = %s '''
    mycursor.execute(sql, id)
    etat = mycursor.fetchone()
    return render_template('admin/commandes/detail/show.html', articles=articles, etat=etat)
