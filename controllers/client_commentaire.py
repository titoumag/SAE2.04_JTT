#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_commentaire = Blueprint('client_commentaire', __name__,
                        template_folder='templates')

@client_commentaire.route('/client/comment/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    avis = request.form.get("commentaire",None)
    note = int(request.form.get("note",None))
    userId = request.form.get('idUser', None)

    mycursor.execute("INSERT INTO avis(casque_id,user_id,texte,note) VALUES(%s,%s,%s,%s)",(article_id,userId,avis,note))
    get_db().commit()

    return redirect('/client/article/details/'+article_id)
    #return redirect(url_for('client_article_details', id=int(article_id)))

@client_commentaire.route('/client/comment/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    userId = request.form.get('idUser', None)

    mycursor.execute("DELETE FROM avis WHERE casque_id=%s AND user_id=%s",(article_id,userId))
    get_db().commit()

    return redirect('/client/article/details/'+article_id)
    #return redirect(url_for('client_article_details', id=int(article_id)))