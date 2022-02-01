#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_info = Blueprint('client_info', __name__,
                        template_folder='templates')

@client_info.route('/client/info/show')
def client_info_show():
    mycursor = get_db().cursor()
    user_id=session["user_id"]

    sql="select * from user where id=%s"
    mycursor.execute(sql,(user_id))
    user=mycursor.fetchone()
    print(user)

    return render_template('/client/info/show.html',user=user)

@client_info.route('/client/info/edit', methods=['GET'])
def client_info_edit():
    mycursor = get_db().cursor()
    user_id=session["user_id"]

    sql="select * from user where id=%s"
    mycursor.execute(sql,(user_id))
    user=mycursor.fetchone()
    print(user)

    return render_template('/client/info/edit.html',user=user)

@client_info.route('/client/info/edit', methods=['POST'])
def client_info_edit_recoit():
    mycursor = get_db().cursor()
    user_id=session["user_id"]
    nom=request.form.get('nom')
    prenom = request.form.get('prenom')
    username = request.form.get('username')
    email = request.form.get('email')
    carte_numero = request.form.get('carte_numero')
    carte_code = request.form.get('carte_code')

    sql="update user set nom=%s,prenom=%s,username=%s,email=%s,carte_numero=%s,carte_code=%s where id=%s"
    tuple=(nom,prenom,username,email,carte_numero,carte_code,user_id)
    mycursor.execute(sql,tuple)
    get_db().commit()

    return redirect('/client/info/show')