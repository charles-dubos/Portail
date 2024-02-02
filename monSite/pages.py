from flask import Blueprint, redirect, render_template, request, url_for
from monSite.functions.general import *

# BLUEPRINTS
bp=Blueprint("pages", __name__)


@bp.route('/')
def index():
    """Page principale -> redirection vers la page paramétrée
    """
    return redirect(Database(DATABASE_NAME).getConfig()['mainPage'])


@bp.route('/<path>', methods=['GET','POST'])
def main(path):
    """Page par identifiant de famille
    """
    global database

    if request.method == 'POST':
        postKey=list(request.form.keys())[0]
        if postKey in database.servers.keys():
            database.servers[postKey].switchState()
        else:
            pass

    return render_template('pages/main.html',
                           path=path,
                           database=database,
                           previous=prevPage(database=database, current=path),
                           next=nextPage(database=database, current=path),
                           ratio=1
                           )


@bp.route('/<path>/edit', methods=['GET','POST'])
def edit(path):
    """Page d'édition par identifiant de famille
    """
    global database

    return render_template('pages/edit.html',
                           path=path,
                           database=database,
                           previous=prevPage(database=database, current=path),
                           next=nextPage(database=database, current=path),
                           ratio=1
                           )
