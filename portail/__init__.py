import os
from flask import Flask, redirect, render_template, request, url_for, send_file, make_response
from flask_minify import Minify
from .functions.general import *
# from .functions.configure import *


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_NAME=os.path.join(app.instance_path, 'monSite.json'),
        LOGFILE_PATH=os.path.join(app.instance_path, 'monSite.log'),
        LOGLEVEL=['NOTSET','DEBUG','INFO','WARNING','ERROR','CRITICAL'][1]
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    # Load config and database
    loadLogging( logConfig=app.config )
    database = loadDatabase( name=app.config['DATABASE_NAME'])


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
        return redirect(
            getCookie(
                database=database,
                name='mainPage')
            )


    @app.route( '/<path>', methods=['GET'] )
    def main(path):
        """Page par identifiant
        """

        return render_template('pages/main.html.j2',
                            path=path,
                            database=database,
                            previous=prevPage( database=database, current=path ),
                            mainPage=getCookie(database=database,name='mainPage'),
                            next=nextPage( database=database, current=path ),
                            ratio=1
                            )


    @app.route( '/<path>/edit', methods=['GET','POST'] )
    def edit(path):
        """Page d'édition par identifiant
        """

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
                            previous=prevPage(database=database, current=path),
                            next=nextPage(database=database, current=path),
                            ratio=1,
                            newNumber=firstAvailable(database=database, current=path),
                            message=message if 'message' in locals() else None
                            )


    @app.route( '/settings', methods=['GET','POST'] )
    def settings():
        """Page de configuration globale
        """

        if request.method == 'POST':
            data = dict( request.form.items( multi=False ) )
            logging.debug( f'Méthode POST utilisée avec les données {data.keys()}' )

            if request.form.get('form') == 'pages':
                logging.info("Enregistrement des pages")
                for pageId in database.getPagesId():
                    database.pages[pageId].title = request.form[f"{pageId}-title"]
                    database.pages[pageId].img =   request.form[f"{pageId}-img"]
                    database.pages[pageId] = database.pages.pop(pageId)
                    logging.debug( f"Enregistrement de {pageId} : titre à {request.form[f"{pageId}-title"]} et image à {request.form[f"{pageId}-img"]}" )
                logging.info('Tri des pages')
                database.sortPages([ pageId[:-6]
                                for pageId in request.form.keys()
                                if pageId.endswith('-title')])

            elif 'delete' in request.form.keys():
                if len( database.pages ) == 1:
                    message = "Impossible de supprimer la page.</br>Il en faut une au minimum."
                elif len( database.pages[ request.form['delete'] ] ) != 0:
                    message = "Impossible de supprimer une page non vide.</br>Supprimez les cartes auparavant."
                else:
                    database.delPage(
                        pageId=request.form['delete'] ) 
            
            elif 'create' in request.form.keys():
                database.newPage(
                    page=Page( {
                        'title': request.form['title'],
                        'img':   request.form['img'],
                        'dictOfCards': {},
                        } )
                      )
                logging.info( f"Création de la page '{request.form['title']}' avec l'image '{request.form['img']}'" )

            elif request.form.get('form') == 'sounds':
                for sound in database.settings['sounds'].keys():
                    database.settings['sounds'][sound]['url'] =    request.form[f"{sound}-url"]
                    database.settings['sounds'][sound]['volume'] = request.form[f"{sound}-volume"]
                    logging.debug( f"Enregistrement de {sound} : url à {request.form[f"{sound}-url"]} et volume à {request.form[f"{sound}-volume"]}" )
        
        return render_template('pages/settings.html.j2',
                            database=database,
                            mainPage=getCookie(database=database,name='mainPage'),
                            message=message if 'message' in locals() else None
                            )
        

    @app.route( '/setcookie', methods=['POST'] )
    def setCookie():
        """Redirection de sauvegarde de cookie
        """
        logging.info("Enregistrement du cookie mainPage")
        response = make_response(redirect('/settings'))
        response.set_cookie( "mainPage", request.form['mainPage'] )
        logging.debug(f"mainPage à {request.form['mainPage']}")
        return response

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


    Minify(app=app, html=True, js=True, cssless=True)
    return app
