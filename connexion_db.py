from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

import pymysql.cursors


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = pymysql.connect(
            host="serveurmysql",
            # host="serveurmysql",
            user="joudot",
            password="3105",
            database="BDD_joudot",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return db


def update_property(attribut, value):
    mycursor = get_db().cursor()
    user_id = session['user_id']

    sql = "select * from user where id=%s"
    print(sql)
    mycursor.execute(sql, (user_id))
    recorded = mycursor.fetchone()[attribut]
    newvalue = float(recorded) + value
    print(recorded, newvalue)
    mycursor.execute("update user set solde=%s where id=%s", (newvalue, user_id))

    if attribut == "solde" and newvalue < 0:
        texte = "Bonjour, vous avez un solde négatif a valeur de :" \
                + str(newvalue) + "€.<br> Veuillez vite le rembourser.<br> " \
                                  "Chaque jour, il y aura un interet de 10%.<br> Merci de votre compréhension.<br> " \
                                  "Cordialement, les gérants du site"
        sql = "INSERT INTO mails(owner_id,sender_id,receiver_id,objetMail,texteMail,dateEnvoi) VALUES (%s,%s,%s,%s,%s,CURDATE())"
        mycursor.execute(sql, (user_id, 1, user_id, "Solde actuel négatif", texte))

    get_db().commit()
