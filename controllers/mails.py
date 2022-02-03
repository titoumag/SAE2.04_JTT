#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import render_template, session, request, flash, redirect

from connexion_db import get_db

mails = Blueprint('mails', __name__,
                  template_folder='templates')


@mails.route('/mails/')
@mails.route('/mails/show')
def mails_show():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT mails.id,receiver.email as receiver,sender.email as sender,texteMail,dateEnvoi,objetMail "
                     "FROM mails "
                     "INNER JOIN user receiver on mails.receiver_id = receiver.id "
                     "INNER JOIN user sender on sender_id = sender.id "
                     "WHERE sender_id = %s OR receiver_id = %s",
                     (session["user_id"], session["user_id"]))
    mails = mycursor.fetchall()
    return render_template('mails/show.html', mails=mails)


@mails.route('/mails/write')
def mails_write():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM user WHERE NOT id = %s", (session['user_id']))
    users = mycursor.fetchall()
    return render_template('mails/write.html', users=users)


@mails.route('/mails/send', methods=['POST'])
def mails_send():
    receiver = request.form.get("receiver_id", None)
    objet = request.form.get("objet", None).replace("\"","\'")
    texte = request.form.get("texte", None).replace("\"","\'")

    texte = replaceAll(texte)

    mycursor = get_db().cursor()
    mycursor.execute(
        "INSERT INTO mails(sender_id,receiver_id,objetMail,texteMail,dateEnvoi) VALUES (%s,%s,%s,%s,CURDATE())",
        (session["user_id"], receiver, objet, texte))
    get_db().commit()
    flash("Votre mail a bien été envoyé !")
    return redirect("/mails/show")


@mails.route('/mails/delete', methods=['GET'])
def mails_delete():
    id = request.args.get('id', '')
    flash("Le mail a été supprimé !")
    mycursor = get_db().cursor()
    mycursor.execute("DELETE FROM mails WHERE id = %s", (int(id)))
    get_db().commit()
    return redirect("/mails/show")

def replaceAll(string):
    newString = ""
    for char in string:
        if char == "'":
            newString+="\\"
        newString+=char
    return newString