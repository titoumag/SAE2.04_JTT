#! /usr/bin/python
# -*- coding:utf-8 -*-
from controllers.mails import *
from controllers.auth_security import *

from controllers.client_article import *
from controllers.client_panier import *
from controllers.client_commande import *
from controllers.client_commentaire import *
from controllers.client_info import *

from controllers.admin_casque import *
from controllers.admin_type_casque import *
from controllers.admin_article import *
from controllers.admin_commande import *
from controllers.admin_main import *
from controllers.admin_users import *

app = Flask(__name__)
app.secret_key = 'PANZERKAMPFWAGEN'
app.config['UPLOAD_FOLDER'] = os.getcwd()+"/static/images/"


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def show_accueil():
    return render_template('auth/mainPage.html')


##################
# Authentification
##################

# Middleware de sécurité

@app.before_request
def before_request():
    if request.path.startswith('/admin') or request.path.startswith('/client'):
        if 'role' not in session:
            return redirect('/login')
            # return redirect(url_for('auth_login'))
        else:
            if (request.path.startswith('/client') and session['role'] != 'ROLE_client') or (
                    request.path.startswith('/admin') and session['role'] != 'ROLE_admin'):
                print('pb de route : ', session['role'], request.path.title(), ' => deconnexion')
                session.pop('username', None)
                session.pop('role', None)
                return redirect('/login')
                # return redirect(url_for('auth_login'))


app.register_blueprint(mails)
app.register_blueprint(auth_security)

app.register_blueprint(client_article)
app.register_blueprint(client_commande)
app.register_blueprint(client_commentaire)
app.register_blueprint(client_panier)
app.register_blueprint(client_info)

app.register_blueprint(admin_article)
app.register_blueprint(admin_type_casque)
app.register_blueprint(admin_casque)
app.register_blueprint(admin_commande)
app.register_blueprint(admin_main)
app.register_blueprint(admin_users)

if __name__ == '__main__':
    app.run()
