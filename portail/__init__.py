import os, logging
from flask import Flask, redirect, render_template, request, url_for, send_file, make_response
from flask_minify import Minify
from .functions.general import loadLogging, getCookie, movePage, initDatabase
from .functions.models import db, SQLCard, SQLPage, SQLSound
from .functions.interface import PageIF, CardIF, SoundIF

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_NAME=os.path.join(app.instance_path, 'monSite.db'),
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

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.config['DATABASE_NAME']}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()
        initDatabase(db=db)


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
        return redirect( str( getCookie(db=db) ) )


    @app.route( '/<pageId>', methods=['GET'] )
    def main(pageId):
        """Page par identifiant
        """

        return render_template('pages/main.html.j2',
                            sounds=SoundIF(db=db).getList(),
                            page=PageIF(db=db, id=pageId).get(),
                            listOfCards=CardIF(db=db,page_id=pageId).getList(),
                            previous=movePage( db=db, page_id=pageId, move=-1 ),
                            next=movePage( db=db, page_id=pageId, move=1 ),
                            ratio=1
                            )


    @app.route( '/<pageId>/edit', methods=['GET','POST'] )
    def edit(pageId):
        """Page d'édition par identifiant
        """

        if request.method == 'POST':
            data = dict( request.form.items( multi=False ) )
            logging.debug( f'Méthode POST utilisée avec les données {data.keys()}' )
            if 'delete-card' in data.keys() :
                CardIF(db=db, id=data['current']).delete()

            elif 'save-card' in data.keys():
                if CardIF(db=db,page_id=pageId,id=data['current']).get().number == data['number']\
                or CardIF(db=db).isAvailable(data['number']):
                    CardIF(db=db, page_id=pageId, id=data['current']).update(
                        number=data['number'],
                        name=data['name'],
                        logo_url=data['logo_url'],
                        link_url=data['link_url']
                    )
                else:
                    message = f"Impossible de changer le numéro de la carte de '{data['current']}'.</br>Le numéro '{data['number']}' est déjà attribué."
                    
            elif 'new-card' in data.keys():
                if CardIF(db=db).isAvailable(data['number']):
                    CardIF(db=db, page_id=pageId).create(
                        number=data['number'],
                        name=data['name'],
                        logo_url=data['logo_url'],
                        link_url=data['link_url']
                    )
                else:
                    message = f"Impossible de créer la carte avec le numéro '{data['number']}'.</br>Le numéro '{data['number']}' est déjà attribué."
            
        return render_template('pages/edit.html.j2',
                            sounds=SoundIF(db=db).getList(),
                            page=PageIF(db=db, id=pageId).get(),
                            listOfCards=CardIF(db=db,page_id=pageId).getList(),
                            previous=movePage( db=db, page_id=pageId, move=-1 ),
                            next=movePage( db=db, page_id=pageId, move=1 ),
                            newNumber = CardIF(db=db,page_id=pageId).firstNumberAvailable()
                            )


    @app.route( '/settings', methods=['GET','POST'] )
    def settings():
        """Page de configuration globale
        """
        activeTabIndex=0

        if request.method == 'POST':
            data = dict( request.form.items( multi=False ) )
            logging.debug( f'Méthode POST utilisée avec les données {data.keys()}' )

            if request.form.get('form') == 'pages':
                logging.info("Enregistrement des pages")

                pagesOrder = [ int(pageId[:-6])
                                for pageId in request.form.keys()
                                if pageId.endswith('-title') and not pageId=="new-title"]

                for page in PageIF(db=db).getList():
                    PageIF(db=db,id=page.id).update(
                        title=request.form[f"{page.id}-title"],
                        background_url=request.form[f"{page.id}-background_url"],
                        order=pagesOrder.index(page.id)
                    )
                    logging.debug( f"Enregistrement de {page.id} : titre à {request.form[f"{page.id}-title"]} et image à {request.form[f"{page.id}-background_url"]}" )
                activeTabIndex=1

            elif request.form.get('form') == 'newPage':
                page = PageIF(db=db).create(
                    title=request.form['new-title'],
                    background_url=request.form['new-background_url']
                )
                logging.info( f"Création de la page {page.id} : '{request.form['new-title']}' avec l'image '{request.form['new-background_url']}'" )
                activeTabIndex=1

            elif 'delete' in request.form.keys():
                if len( PageIF(db).getList() ) == 1:
                    message = "Impossible de supprimer la page.</br>Il en faut une au minimum."
                elif len( CardIF(db=db,page_id=request.form['delete']).getList() ) != 0:
                    message = "Impossible de supprimer une page non vide.</br>Supprimez les cartes auparavant."
                else:
                    PageIF(db=db,id=request.form['delete']).delete()
                activeTabIndex=1
            
            elif request.form.get('form') == 'sounds':
                for sound in SoundIF(db=db).getList():
                    SoundIF(db=db,context=sound.context).update(
                        url=request.form[f"{sound.context}-url"],
                        volume=request.form[f"{sound.context}-volume"],
                    )
                    logging.debug( f"Enregistrement de {sound.context} : url à {request.form[f"{sound.context}-url"]} et volume à {request.form[f"{sound.context}-volume"]}" )
                activeTabIndex=2
        
        return render_template('pages/settings.html.j2',
                            sounds=SoundIF(db=db).getList(),
                            pages=PageIF(db=db).getList(),
                            mainPage=getCookie(db=db),
                            message=message if 'message' in locals() else None,
                            activeTabIndex=activeTabIndex
                            )
        
#    @app.after_request
#    def add_header(r):
#        """
#        Add headers to both force latest IE rendering engine or Chrome Frame,
#        and also to cache the rendered page for 10 minutes.
#        """
#
#        r.headers["Pragma"] = "no-cache"
#        r.headers["Expires"] = "0"
#        r.headers['Cache-Control'] = 'public, max-age=0'
#        return r


    Minify(app=app, html=True, js=True, cssless=True)
    return app
