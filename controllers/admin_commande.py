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
    sql = "SELECT commande.id, username, SUM(quantite) as commande_quantite,SUM(quantite*prix_unit)*valeurAjoute+clic as prix_tot, etat_id, date_achat,etat.libelle " \
          "FROM ligne_commande " \
          "INNER JOIN commande on commande.id=ligne_commande.commande_id " \
          "INNER JOIN user on user.id = commande.user_id " \
          "INNER JOIN etat on etat.id = commande.etat_id " \
          "INNER JOIN type_livraison ON type_livraison_id=type_livraison.id " \
          "GROUP BY commande.id " \
          "ORDER BY etat_id,user_id,date_achat"
    mycursor.execute(sql)
    commandes = mycursor.fetchall()
    print(commandes)

    return render_template('admin/commandes/show.html', commandes=commandes)


@admin_commande.route('/admin/commande/valider/<int:id>', methods=['get', 'post'])
def admin_commande_valider(id):
    mycursor = get_db().cursor()
    sql = '''UPDATE commande SET etat_id=2 WHERE commande.id=%s'''
    mycursor.execute(sql, id)

    mycursor.execute("SELECT * FROM commande WHERE id = %s",(id))
    commande = mycursor.fetchone()
    mycursor.execute(
        "INSERT INTO mails(sender_id,receiver_id,objetMail,texteMail,dateEnvoi) VALUES (%s,%s,%s,%s,CURDATE())",
        (1, int(commande["user_id"]), "Validation de la commande n°"+str(id), "Bonjour, votre commande a été validée."))
    get_db().commit()
    return redirect('/admin/commande/show')


@admin_commande.route('/admin/commande/<int:id>', methods=['get', 'post'])
def admin_commande_details(id):
    mycursor = get_db().cursor()
    sql = "select commande_id, modele.libelle as libelle, prix_unit, quantite, prix_unit*quantite as prix_tot, couleur.libelle as cl, taille.libelle as tl " \
          "from ligne_commande " \
          "INNER JOIN casque on casque.id = casque_id " \
          "INNER JOIN modele on modele.id = casque.modele_id " \
          "INNER JOIN couleur ON couleur.id=casque.couleur_id "\
            "INNER JOIN taille ON taille.id=casque.taille_id  "\
          "where commande_id = %s "
    mycursor.execute(sql, id)
    articles = mycursor.fetchall()
    sql = "select libelle, al.ville, al.code, al.rue,al.numero , af.ville,af.code ,af.rue,af.numero " \
          "from etat " \
          "inner join commande on commande.etat_id = etat.id " \
          "INNER JOIN adresse AS al ON adresse_id_livraison=al.id " \
          "INNER JOIN adresse AS af ON adresse_id_facturation=af.id " \
          "where commande.id = %s "
    mycursor.execute(sql, id)
    etat = mycursor.fetchone()
    return render_template('admin/commandes/detail/show.html', articles=articles, etat=etat)
