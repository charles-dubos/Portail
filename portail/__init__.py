import os, logging, traceback
from flask import Flask, redirect, render_template, request, url_for, send_file, make_response, Response
from flask_minify import Minify
from .functions import  getCookie, movePage, initDatabase,\
                        db, SQLCard, SQLPage, SQLSound, \
                        PageIF, CardIF, SoundIF

def create_app(test_config=None) -> Flask:
    """Creation of Flask app.

    Args:
        test_config (_type_, optional): Testing config file. Defaults to None.

    Returns:
        Flask: Generated Flask app.
    """

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=getattr( logging, os.getenv('PORTAIL_LOGLEVEL', 'INFO') )
    )


    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('PORTAIL_SECRETKEY', 'dev')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    # Load database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{
        os.getenv('PORTAIL_SQLITE_FILE', os.path.join(app.instance_path, 'monSite.db'))
    }'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()
        initDatabase(db=db)


    @app.route('/manifest.json')
    def serve_manifest() -> Response:
        """Manifest to install web app on client.

        Returns:
            Response: Corresponding file.
        """
        return send_file('manifest.json', mimetype='application/manifest+json')

    @app.route('/sw.js')
    def serve_sw() -> Response:
        """Installs the workers service.

        Returns:
            Response: Return sw.js file.
        """
        return send_file('sw.js', mimetype='application/javascript')


    @app.route('/')
    def index() -> Response:
        """Main page, set by cookie if exists.

        Returns:
            Response: Redirect to path from cookie.
        """
        return redirect( str( getCookie(db=db) ) )


    @app.route( '/<pageId>', methods=['GET'] )
    def main(pageId:int) -> Response:
        """Page for corresponding page ID.

        Args:
            pageId (int): Id of page in database.

        Returns:
            Response: Serves the corresponding HTML page from template.
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
    def edit(pageId:int) -> Response:
        """Edit page for corresponding page ID (allowing get and posts HTML methods).

        Args:
            pageId (int): Id of page in database.

        Returns:
            Response: Serves the corresponding HTML page from template.
        """
        message = ""

        if request.method == 'POST':
            data = dict( request.form.items( multi=False ) )
            logging.debug( f'Méthode POST utilisée avec les données {data.keys()}' )
            if 'delete-card' in data.keys() :
                try:
                    CardIF(db=db, id=data['current']).delete()
                except Exception:
                    message += f"Impossible de supprimer la carte {data['name']}"

            elif 'save-card' in data.keys():
                try:
                    CardIF(db=db, page_id=pageId, id=data['current']).update(
                        number=data['number'],
                        name=data['name'],
                        logo_url=data['logo_url'],
                        link_url=data['link_url']
                    )
                except Exception:
                    message += f"Impossible d'enregistrer la carte {data['name']}"
                    
            elif 'new-card' in data.keys():
                try:
                    CardIF(db=db, page_id=pageId).create(
                        number=data['number'],
                        name=data['name'],
                        logo_url=data['logo_url'],
                        link_url=data['link_url']
                    )
                except Exception:
                    message += f"Impossible de créer la carte {data['name']}"
            
        if message: logging.warn(message)

        return render_template('pages/edit.html.j2',
                            sounds=SoundIF(db=db).getList(),
                            page=PageIF(db=db, id=pageId).get(),
                            listOfCards=CardIF(db=db,page_id=pageId).getList(),
                            previous=movePage( db=db, page_id=pageId, move=-1 ),
                            next=movePage( db=db, page_id=pageId, move=1 ),
                            newNumber = CardIF(db=db,page_id=pageId).firstNumberAvailable(),
                            message=message,
                            ratio=1
                            )


    @app.route( '/settings', methods=['GET','POST'] )
    def settings() -> Response:
        """Setting page (allowing get and posts HTML methods).

        Returns:
            Response: Serves the corresponding HTML page from template.
        """
        activeTabIndex=0
        message = ""

        if request.method == 'POST':
            data = dict( request.form.items( multi=False ) )
            logging.debug( f'Méthode POST utilisée avec les données {data.keys()}' )
            activeTabIndex=1

            if request.form.get('form') == 'pages':
                logging.info("Enregistrement des pages")

                pagesOrder = [ int(pageId[:-6])
                                for pageId in request.form.keys()
                                if pageId.endswith('-title') and not pageId=="new-title"]

                for page in PageIF(db=db).getList():
                    PageIF(db=db,id=page.id).update(
                        title=request.form[f"{page.id}-title"],
                        background_url=request.form[f"{page.id}-background_url"],
                        order=pagesOrder.index(page.id)+1
                    )
                    logging.debug( f"Enregistrement de {page.id} : titre à {request.form[f"{page.id}-title"]} et image à {request.form[f"{page.id}-background_url"]}" )

            elif request.form.get('form') == 'newPage':
                try:
                    page = PageIF(db=db).create(
                        title=request.form['new-title'],
                        background_url=request.form['new-background_url']
                    )
                    logging.info( f"Création de la page {page.id} : '{request.form['new-title']}' avec l'image '{request.form['new-background_url']}'" )
                except Exception:
                    message += f"Impossible de créer la page {request.form['new-title']}"

            elif 'delete' in request.form.keys():
                try:
                    PageIF(db=db,id=request.form['delete']).delete()
                except Exception:
                    message += ("Impossible de supprimer la page " + request.form[f'{request.form['delete']}-title'])
            
            elif request.form.get('form') == 'sounds':
                activeTabIndex=2
                for sound in SoundIF(db=db).getList():
                    try:
                        SoundIF(db=db,context=sound.context).update(
                            url=request.form[f"{sound.context}-url"],
                            volume=request.form[f"{sound.context}-volume"],
                        )
                        logging.debug( f"Enregistrement de {sound.context} : url à {request.form[f"{sound.context}-url"]} et volume à {request.form[f"{sound.context}-volume"]}" )
                    except Exception:
                        message += f"Impossible modifier les sons."

        if message: logging.warn(message)
        
        return render_template('pages/settings.html.j2',
                            sounds=SoundIF(db=db).getList(),
                            pages=PageIF(db=db).getList(),
                            mainPage=getCookie(db=db),
                            message=message if 'message' in locals() else None,
                            activeTabIndex=activeTabIndex
                            )
        
    @app.route( '/health', methods=['GET'] )
    def health() -> Response:
        return 'OK', 200
        
    Minify(app=app, html=True, js=True, cssless=True)
    return app
