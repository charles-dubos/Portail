from flask import Flask, redirect, render_template, request, url_for, send_file, make_response
from functions.general import *

setCookie=False

app = Flask( __name__ )

@app.before_request
def before_request_func():
    global config
    global database
    global setCookie

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
    """Page par identifiant de famille
    """
    global database

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
    """Page d'édition par identifiant de famille
    """
    global database
    message = None

    if request.method == 'POST':
        data = dict( request.form.items( multi=False ) )
        logging.debug( f'Méthode POST utilisée avec les données {data.keys()}' )

        if 'delete-card' in data.keys() :
            deleteCard(
                database=database,
                familyId=path,
                cardId=data['current']
            )
            database.save()

        elif 'save-card' in data.keys():
            if data['current'] != data['number']:
                if data['number'] in database.families[path].dictOfCards.keys():
                    message = f"Impossible de changer le numéro de la carte de '{data['current']}'.</br>Le numéro '{data['number']}' est déjà attribué."
                else:
                    deleteCard(
                        database=database,
                        familyId=path,
                        cardId=data['current']
                    )
                    data['current'] = data['number']
            editCard(
                database=database,
                familyId=path,
                cardId=data['current'],
                data=data
            )
            database.save(sortFamily=path)
                
        elif 'new-card' in data.keys():
            if data['number'] in database.families[path].dictOfCards.keys():
                message = f"Impossible de créer la carte avec le numéro '{data['number']}'.</br>Le numéro '{data['number']}' est déjà attribué."
            else:
                editCard(
                    database=database,
                    familyId=path,
                    cardId=data['number'],
                    data=data
                )
                database.save(sortFamily=path)

        elif 'save-conf' in data.keys():
            logging.info( f"Enregistrement des configurations" )
            logging.debug( f"{config.getCfg('mainPage')}")
            if logging.debug(data['mainPage']) != config.getCfg('mainPage'):
                config.setCfg( key='mainPage', value=data['mainPage'] )
                logging.debug( f"Enregistrement de mainPage à la valeur {data['mainPage']}" )
                global setCookie
                setCookie=True
            
            for sound in database.settings['sounds']:
                    database.settings['sounds'][sound]['url'] = data[f"{sound}-url"]
                    database.settings['sounds'][sound]['volume'] = data[f"{sound}-volume"]
                    logging.debug( f"Enregistrement de {sound} : url à {data[f"{sound}-url"]} et volume à {data[f"{sound}-volume"]}" )
            database.save()

        elif 'save-fam' in data.keys():
            if path != data['famId']:
                if data['famId'] in database.families.keys():
                    message = f"Impossible de changer la famille de '{path}'.</br>Le nom '{data['famId']}' est déjà attribué."
                else:
                    logging.info( f"Déplacement de la famille {path} vers {data['famId']}" )
                    database.newFamily(
                        familyId=data['famId'],
                        family=database.delFamily( familyId=path )
                    )
                    path = data['famId']
            if database.families[path].title != data['title']:
                logging.debug( f"Mise à jour de {database.families[path].title} en {data['title']}" )
                database.families[path].title = data['title']
            if database.families[path].img != data['img']:
                logging.debug( f"Mise à jour de {database.families[path].img} en {data['img']}" )
                database.families[path].img = data['img']
            database.save()

        elif 'delete-fam' in data.keys():
            if len( database.families ) == 1:
                message = "Impossible de supprimer la famille.</br>Il en faut une au minimum."
            elif len( database.families[path] ) != 0:
                message = "Impossible de supprimer une famille non vide.</br>Supprimez les cartes auparavant."
            else:
                path = nextPage( database=database, current=path )
                database.delFamily( familyId=data['famId'] )

        elif 'new-fam' in data.keys():
            if data['famId'] in database.families.keys():
                message = f"Impossible de créer la famille.</br>L'identifiant '{data['famiId']}' déjà utilisé."
            else:
                logging.info( f"Création de la famille {data['famId']}" )
                logging.debug( f"avec les valeurs '{data['title']}', '{data['img']}'" )
                database.newFamily(
                    familyId=data['famId'],
                    family=Family( {
                        'title': data['title'],
                        'img': data['img'],
                        'dictOfCards': {},
                    } )
                )
                path = data['famId']

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
