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

    return render_template('/client/info/show.html',user=user)

@client_info.route('/client/info/edit', methods=['GET'])
def client_info_edit():
    mycursor = get_db().cursor()
    user_id=session["user_id"]

    sql="select * from user where id=%s"
    mycursor.execute(sql,(user_id))
    user=mycursor.fetchone()

    return render_template('/client/info/edit.html',user=user)

@client_info.route('/client/info/edit', methods=['POST'])
def client_info_edit_recoit():
    mycursor = get_db().cursor()
    user_id=session["user_id"]
    nom=request.form.get('nom')
    prenom = request.form.get('prenom')
    username = request.form.get('username')
    email = request.form.get('email')

    sql="update user set nom=%s,prenom=%s,username=%s,email=%s where id=%s"
    tuple=(nom,prenom,username,email,user_id)
    mycursor.execute(sql,tuple)
    get_db().commit()

    return redirect('/client/info/show')

@client_info.route('/client/info/add_money', methods=['POST'])
def client_info_add_money_recoit():
    mycursor = get_db().cursor()
    argent = int(request.form.get('argent'))
    user_id = session["user_id"]
    sql = "select * from user where id=%s"
    mycursor.execute(sql, (user_id))
    user = mycursor.fetchone()
    argent += user['solde']

    sql = "update user set solde=%s where id=%s"
    tuple = (argent, user_id)
    mycursor.execute(sql, tuple)
    get_db().commit()

    return redirect('/client/info/show')

@client_info.route('/client/info/add_money')
def client_info_add_money():
    mycursor = get_db().cursor()
    user_id = session["user_id"]
    sql = "select * from user where id=%s"
    mycursor.execute(sql,(user_id))
    user=mycursor.fetchone()

    return render_template('/client/info/add_money.html',user=user)