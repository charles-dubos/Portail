from flask import Flask, redirect, render_template, request, url_for, send_file, make_response
from functions.general import *
from functions.configure import *

setCookie=False

app = Flask( __name__ )

@app.before_request
def before_request_func():
    # global config
    # global database
    # global setCookie
    message = None

    if not config.isSet():
        logging.info('Récupération du cookie de conf')
        if not config.loadFromCookies( database=database ):
            setCookie=True

@app.after_request
def after_request_func(response):
    global setCookie
    if setCookie:
        response.set_cookie(
            key='config',
            value=config.dumps(),
            secure=True,
            samesite="Strict"
        )
        setCookie=False
    return response


@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')

@app.route('/')
def index():
    """Page principale ->  récupération du cookie de conf et redirection vers la page paramétrée
    """
    pageRedirect = redirect(config.getCfg('mainPage'))

    return pageRedirect


@app.route( '/<path>', methods=['GET'] )
def main(path):
    """Page par identifiant
    """

    return render_template('pages/main.html.j2',
                           path=path,
                           database=database,
                           config=config,
                           previous=prevPage( database=database, current=path ),
                           next=nextPage( database=database, current=path ),
                           ratio=1
                           )


@app.route( '/<path>/edit', methods=['GET','POST'] )
def edit(path):
    """Page d'édition par identifiant
    """
    # global database
    message = None

    if request.method == 'POST':
        data = dict( request.form.items( multi=False ) )
        logging.debug( f'Méthode POST utilisée avec les données {data.keys()}' )

        if 'delete-card' in data.keys() :
            deleteCard(
                database=database,
                pageId=path,
                cardId=data['current']
            )

        elif 'save-card' in data.keys():
            if data['current'] != data['number'] and data['number'] in database.pages[path].dictOfCards.keys():
              message = f"Impossible de changer le numéro de la carte de '{data['current']}'.</br>Le numéro '{data['number']}' est déjà attribué."
            else:
                saveCard(
                    database=database,
                    pageId=path,
                    data=data
                )
                
        elif 'new-card' in data.keys():
            if data['number'] in database.pages[path].dictOfCards.keys():
                message = f"Impossible de créer la carte avec le numéro '{data['number']}'.</br>Le numéro '{data['number']}' est déjà attribué."
            else:
                editCard(
                    database=database,
                    pageId=path,
                    cardId=data['number'],
                    data=data
                )
                database.save(sortPage=path)

    return render_template('pages/edit.html.j2',
                           path=path,
                           database=database,
                           config=config,
                           previous=prevPage(database=database, current=path),
                           next=nextPage(database=database, current=path),
                           ratio=1,
                           newNumber=firstAvailable(database=database, current=path),
                           message=message
                           )


@app.route( '/settings', methods=['GET','POST'] )
def settings():
    """Page de configuration globale
    """
    # global database
    message = None

    if request.method == 'POST':
        data = dict( request.form.items( multi=False ) )
        logging.debug( f'Méthode POST utilisée avec les données {data.keys()}' )

        if 'save-conf' in data.keys():
            global setCookie
            setCookie = saveConfig(
                database=database,
                config=config,
                data=data
            )
        
        elif any(item.endswith('-delete') for item in data.keys()):
            pageName = next((s[:-7] for s in data.keys() if s.endswith('-delete')),None)
            if len( database.pages ) == 1:
                message = "Impossible de supprimer la page.</br>Il en faut une au minimum."
            elif len( database.pages[pageName]) != 0:
                message = "Impossible de supprimer une page non vide.</br>Supprimez les cartes auparavant."
            else:
                path = deletePage(
                    database=database,
                    data=data,
                    pageName=pageName
                )

        elif 'new-fam' in data.keys():
            path = createPage(
                database=database,
                data=data
            )

    return render_template('pages/settings.html.j2',
                        database=database,
                        config=config,
                        message=message
    )


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
