from flask import Blueprint, redirect, render_template, request
from monSite.functions.general import *

# BLUEPRINTS
bp=Blueprint("pages", __name__)

@bp.route('/')
def index():
    """Page principale
    """
    return redirect(Database(DATABASE_NAME).getConfig()['mainPage'])

@bp.route('/<path>', methods=['GET','POST'])
def main(path):
    """Page par identifiant de lien
    """
    global database

    if request.method == 'POST':
        postKey=list(request.form.keys())[0]
        if postKey in database.servers.keys():
            database.servers[postKey].switchState()
        else:
            pass

    return render_template('pages/main.html',
                           title=getTitle(database=database, current=path),
                           previous=prevPage(database=database, current=path),
                           home=database.getConfig()['mainPage'],
                           next=nextPage(database=database, current=path),
                           dictOfServers=database.getServers(),
                           family=database.families[path],
                           ratio=1,
                           modeSombre=database.config['modeSombre']
                           )

# EDIT
