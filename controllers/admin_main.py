#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_main = Blueprint('admin_main', __name__,
                        template_folder='templates')


@admin_main.route('/admin/main')
def admin_mainPage():
    cursor = get_db().cursor()
    cursor.execute("SELECT user.username as name, user.solde as total FROM user ORDER BY total")
    user = cursor.fetchone()

    cursor.execute("SELECT SUM(quantite*prix_unit)*valeurAjoute+clic as chiffreAffaire "
                   "FROM commande "
                   "INNER JOIN ligne_commande ON ligne_commande.commande_id=commande.id "
                   "INNER JOIN type_livraison ON type_livraison_id=type_livraison.id "
                   "GROUP BY commande.id")
    tab = cursor.fetchall()
    chiffreAffaire = 0.0
    for commande in tab:
        chiffreAffaire+=float(commande["chiffreAffaire"])
    return render_template('admin/main/admin_main.html', user=user,chiffreAffaire=chiffreAffaire)