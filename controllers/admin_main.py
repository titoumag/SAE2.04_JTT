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
    cursor.execute("SELECT user.username as name, user.solde as total FROM user ORDER BY total DESC")
    user = cursor.fetchone()

    cursor.execute("SELECT SUM(quantite*prix_unit) as chiffreAffaire FROM ligne_commande")
    chiffreAffaire = cursor.fetchone()["chiffreAffaire"]
    return render_template('admin/main/admin_main.html', user=user,chiffreAffaire=chiffreAffaire)