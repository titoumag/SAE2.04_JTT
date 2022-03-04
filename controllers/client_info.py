#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db,update_property

client_info = Blueprint('client_info', __name__,
                        template_folder='templates')

@client_info.route('/client/info/show')
def client_info_show():
    mycursor = get_db().cursor()
    user_id=session["user_id"]

    sql="select * from user where id=%s"
    mycursor.execute(sql,(user_id))
    user=mycursor.fetchone()

    #sql="select * from liste_adresse inner join adresse on liste_adresse.Id_Adresse=adresse.id  where Id_User=%s"
    sql = "select * from adresse where user_id=%s"
    mycursor.execute(sql,(user_id))
    adresse=mycursor.fetchall()

    mycursor.execute("SELECT * from coupons where user_id = %s",user_id)
    coupons = mycursor.fetchall()

    if 'clic' in session:
        session['clic'] += 1
    return render_template('/client/info/show.html',user=user,liste=adresse,coupons=coupons)

@client_info.route('/client/info/edit', methods=['GET'])
def client_info_edit():
    mycursor = get_db().cursor()
    user_id=session["user_id"]

    sql="select * from user where id=%s"
    mycursor.execute(sql,(user_id))
    user=mycursor.fetchone()

    if 'clic' in session:
        session['clic'] += 1
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
    argent = int(request.form.get('argent',None))*0.9

    if argent > 9999999999.99:
        argent = 9999999999.99

    if argent < -9999999999.99:
        argent = -9999999999.99

    update_property("solde",argent)

    return redirect('/client/info/show')

@client_info.route('/client/info/add_money')
def client_info_add_money():
    mycursor = get_db().cursor()
    user_id = session["user_id"]
    sql = "select * from user where id=%s"
    mycursor.execute(sql,(user_id))
    user=mycursor.fetchone()

    if 'clic' in session:
        session['clic'] += 1
    return render_template('/client/info/add_money.html',user=user)

@client_info.route('/client/info/delete_adresse',methods=['POST'])
def client_info_delete_adresse():
    mycursor = get_db().cursor()
    user_id = session["user_id"]
    adresse= request.form.get('adresse')

    #sql = "delete from liste_adresse where Id_User=%s and Id_Adresse=%s"
    sql = "delete from adresse where id=%s"
    mycursor.execute(sql, (adresse))
    get_db().commit()

    return redirect('/client/info/show')

@client_info.route('/client/info/add_adresse')
def client_info_add_adresse():
    mycursor = get_db().cursor()
    user_id = session["user_id"]
    sql = "select * from user where id=%s"
    mycursor.execute(sql,(user_id))
    user=mycursor.fetchone()

    if 'clic' in session:
        session['clic'] += 1
    return render_template('/client/info/add_adresse.html',user=user)

@client_info.route('/client/info/add_adresse',methods=['POST'])
def client_info_add_adresse_recoit():
    mycursor = get_db().cursor()
    user_id = session["user_id"]
    ville = request.form.get('ville')
    rue = request.form.get('rue')
    numero = request.form.get('numero')
    code= request.form.get('code')

    sql = "insert into adresse values (null,%s,%s,%s,%s,%s)"
    mycursor.execute(sql, (user_id,ville,rue,numero,code))
    get_db().commit()
    id = mycursor.lastrowid

    # sql = "insert into liste_adresse values (%s,%s)"
    # mycursor.execute(sql, (user_id, id))
    # get_db().commit()

    return redirect('/client/info/show')

@client_info.route('/client/info/edit_adresse')
def client_info_edit_adresse():
    mycursor = get_db().cursor()
    user_id = session["user_id"]
    adresse_id=request.args.get('adresse')

    sql = "select * from user where id=%s"
    mycursor.execute(sql,(user_id))
    user=mycursor.fetchone()
    sql = "select * from adresse where id=%s"
    mycursor.execute(sql, (adresse_id))
    adresse = mycursor.fetchone()

    if 'clic' in session:
        session['clic'] += 1
    return render_template('/client/info/edit_adresse.html',user=user,adresse=adresse)

@client_info.route('/client/info/edit_adresse',methods=['POST'])
def client_info_edit_adresse_recoit():
    mycursor = get_db().cursor()
    user_id = session["user_id"]
    ville = request.form.get('ville')
    rue = request.form.get('rue')
    numero = request.form.get('numero')
    code= request.form.get('code')
    adresse_id = request.form.get('id')

    sql = "update adresse set ville=%s,rue=%s,numero=%s,code=%s where id=%s"
    mycursor.execute(sql, (ville,rue,numero,code,adresse_id))
    get_db().commit()

    return redirect('/client/info/show')