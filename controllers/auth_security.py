#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
import random

from connexion_db import get_db

auth_security = Blueprint('auth_security', __name__,
                        template_folder='templates')


@auth_security.route('/login')
def auth_login():
    return render_template('auth/login.html')


@auth_security.route('/login', methods=['POST'])
def auth_login_post():
    mycursor = get_db().cursor()
    username = request.form.get('username')
    password = request.form.get('password')
    tuple_select = (username)
    sql = '''SELECT * FROM user WHERE username LIKE %s'''
    mycursor.execute(sql, tuple_select)
    user = mycursor.fetchone()
    if user:
        mdp_ok = check_password_hash(user['password'], password)
        if not mdp_ok:
            flash(u'Vérifier votre mot de passe et essayer encore.')
            return redirect('/login')
        else:
            session['username'] = user['username']
            session['role'] = user['role']
            session['user_id'] = user['id']
            session['clic'] = 0
            print(user['username'], user['role'])
            if user['role'] == 'ROLE_admin':
                return redirect('/admin/main')
            else:
                return redirect('/client/article/show')
    else:
        flash(u'Vérifier votre login et essayer encore.')
        return redirect('/login')

@auth_security.route('/signup')
def auth_signup():
    return render_template('auth/signup.html')

@auth_security.route('/info')
def info():
    return render_template('info/info.html')

@auth_security.route('/pub')
def pub():
    return render_template('info/pub.html', image="Scams/scam"+str(random.randint(1,9))+".gif")


@auth_security.route('/signup', methods=['POST'])
def auth_signup_post():
    mycursor = get_db().cursor()
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    tuple_select = (username, email)
    sql = '''SELECT * FROM user WHERE username LIKE %s AND email LIKE %s'''
    mycursor.execute(sql, tuple_select)
    user = mycursor.fetchone()
    if user:
        flash(u'votre adresse Email ou  votre Username(login) existe déjà')
        return redirect('/signup')

    # ajouter un nouveau user
    password = generate_password_hash(password, method='sha256')
    tuple_insert = (username, email, password, 'ROLE_client',1,nom,prenom,0)
    sql = '''INSERT INTO user (username,email,password,role,est_actif,nom,prenom,solde) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()                    # position de cette ligne discutatble !
    sql='''SELECT last_insert_id()'''
    mycursor.execute(sql)
    info_last_id = mycursor.fetchone()
    user_id = info_last_id['last_insert_id()']
    get_db().commit()
    session.pop('username', None)
    session.pop('role', None)
    session.pop('user_id', None)
    session['username'] = username
    session['role'] = 'ROLE_client'
    session['user_id'] = user_id
    session['clic'] = 0
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@auth_security.route('/logout')
def auth_logout():
    session.pop('username', None)
    session.pop('role', None)
    session.pop('user_id', None)
    session.pop('clic',None)
    return redirect('/')
    #return redirect(url_for('main_index'))

@auth_security.route('/forget-password', methods=['GET'])
def forget_password():
    return render_template('auth/forget_password.html')


@auth_security.route('/loginForgot', methods=['POST'])
def auth_loginForgot_post():
    mycursor = get_db().cursor()
    username = request.form.get('username')
    mail = request.form.get('mail')
    tuple_select = (username,mail)
    sql = '''SELECT * FROM user WHERE username LIKE %s AND email LIKE %s'''
    mycursor.execute(sql, tuple_select)
    user = mycursor.fetchone()
    if user:
        flash(u'Un mail (facturé à 50€) a été envoyé à '+mail+" .")
        mycursor.execute("UPDATE user SET solde = %s WHERE id = %s",(user["solde"]-50,user["id"]))
        mycursor.execute("INSERT INTO mails(owner_id,sender_id,receiver_id,objetMail,texteMail,dateEnvoi) VALUES (%s,%s,%s,%s,%s,CURDATE())",
                         (user["id"],1,user["id"],"Oubli de Mot de Passe","Bonjour, merci de vous souvenir de votre mot de passe." ))
        get_db().commit()
        return redirect('/login')
    else:
        flash(u'Vérifier votre login,votre email et essayez encore.')
        return redirect('/loginForgot')
