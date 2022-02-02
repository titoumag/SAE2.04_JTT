#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import render_template, session

from connexion_db import get_db

mails = Blueprint('mails', __name__,
                           template_folder='templates')


@mails.route('/mails/')
@mails.route('/mails/show')
def mails_show():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT receiver.email as receiver,sender.email as sender,texteMail,dateEnvoi,objetMail "
                     "FROM mails "
                     "INNER JOIN user receiver on mails.receiver_id = receiver.id "
                     "INNER JOIN user sender on sender_id = sender.id "
                     "WHERE sender_id = %s OR receiver_id = %s",
                     (session["user_id"],session["user_id"]))
    mails = mycursor.fetchall()
    if session["role"] == "ROLE_client":
        return render_template('client/mails/show.html', mails=mails)
    return render_template('admin/mails/show.html', mails=mails)

@mails.route('/mails/write')
def mails_write():
    return render_template('mails/write.html', mails=mails)