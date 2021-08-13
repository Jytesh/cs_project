from flask import Blueprint,render_template,current_app 
from db_queries import getDress
dresspage_blueprint = Blueprint('dresspage', __name__, template_folder='templates', static_folder='static')

@dresspage_blueprint.route('/dresspage/<dressid>')
def dresspage(dressid):
    mysql = current_app.config['mysql']
    connection=mysql.connection
    dress_info=getDress(connection,dressid)
    
    return render_template('Dresspage.html',
                            dress_name=dress_info[1],
                            description=dress_info[2],
                            dress_image_link=dress_info[3])
      

