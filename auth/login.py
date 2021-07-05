from auth.signup import signup
from flask import Blueprint , request, session, flash, redirect, render_template, url_for, current_app
from flask_mysql_connector import MySQL
from werkzeug.security import check_password_hash

from db_queries import if_user, password_hash_returner


login_blueprint = Blueprint('login', __name__, template_folder="templates", static_folder="static")

@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """ The Login Page """

    mysql = current_app.config['mysql']

    # If the request method is POST (ie the user clicked a button on the page)
    if request.method == 'POST':

        # Getting the inputs
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connection
        # Checking if the user exists in our database
        if if_user(conn, username):
            password_hash = password_hash_returner(conn, username, password)
            # Checking if the password is correct
            if check_password_hash(password_hash, password):
                # Logging in the user if the checks are passed
                session.permanent = True
                session['username'] = username
                flash('Successfully logged in!', 'info')
                conn.close()
                return redirect(url_for('profile'))
            else:
                # Flashing a message if there is a error in the input
                flash('Please check your username and password.', 'info')
                conn.close()
                return redirect(url_for('login'))
        else:
            # Flashing a message is there is no account with the inputed username
            flash("Account doesn't exist", 'info')
            conn.close()
            return redirect(url_for('login'))

    # If the request method is GET (ie The user opened the webpage)
    else:
        # If user is already logged in we redirect to the Profile page
        if 'username' in session:
            flash('Already logged in.', 'info')
            return redirect(url_for('profile'))
        else:
            print(url_for('signup.signup'))
            # If not we show the login page
            return render_template('login.html',
                    homepage_link = url_for('home'),
                    signup_link = url_for('signup.signup')
                )

@login_blueprint.route('/logout')
def logout():
    """ The logout page """
    # Checking if user is logged in 
    if 'username' in session:
        # Deleting the session data
        session.pop('username', None)
        flash('Logged out.')
        return redirect(url_for('home'))
    else:
        # If the user tries to logout without being logged in we flash a message
        flash('Not logged in.')
        return redirect(url_for('home'))