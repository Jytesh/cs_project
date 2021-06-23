from flask import Flask,render_template, url_for, redirect, session
from flask_mysql_connector import MySQL

from datetime import timedelta

# Importing blueprints
from auth.login import login_blueprint
from auth.signup import signup_blueprint

from db_queries import view_all_users

app = Flask(__name__)

app.register_blueprint(login_blueprint)
app.register_blueprint(signup_blueprint)

# Setting up config var for mysql
app.config['MYSQL_USER'] = 'sql6419760'
app.config['MYSQL_HOST'] = 'sql6.freesqldatabase.com'
app.config['MYSQL_DATABASE'] = 'sql6419760'
app.config['MYSQL_PASSWORD'] = 'Y7xYSrHExL'
app.config['MYSQL_PORT'] = '3306'
mysql = MySQL(app)

app.config['mysql'] = mysql

# seckret key dont leak :)
app.secret_key = "Veryvery secret key :). ha"

app.permanent_session_lifetime = timedelta(minutes=10)

@app.route('/')
def home():
    if 'username' in session:
        is_loggedin = True
    else:
        is_loggedin = False

    return render_template('index.html', 
            login_link = url_for('login.login'),
            signup_link = url_for('signup.signup'), 
            logout_link = url_for('login.logout'),
            profile_link = url_for('profile'),
            is_loggedin = is_loggedin
        )

@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        return render_template('profile.html', user=username, homepage_link=url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/dbtest')
def dbtest():
    conn = mysql.connection 
    
    output = view_all_users(conn)

    conn.close()
    return str(output)

if __name__ == '__main__':
   app.run(debug=True)