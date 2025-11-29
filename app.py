from flask import Flask, redirect, render_template, request, url_for, send_from_directory
from functions.general import *

app = Flask( __name__ )

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')

@app.route('/')
def index():
    """Page principale -> redirection vers la page paramétrée
    """
    logging.info('Redirection vers "{}"'.format(
        Database(DATABASE_NAME).config['mainPage']
    ))
    
    return redirect(Database(DATABASE_NAME).config['mainPage'])


@app.route( '/<path>', methods=['GET'] )
def main(path):
    """Page par identifiant de famille
    """
    global database

    return render_template('pages/main.html',
                           path=path,
                           database=database,
                           previous=prevPage( database=database, current=path ),
                           next=nextPage( database=database, current=path ),
                           ratio=1
                           )


@app.route( '/authenticated/<path>', methods=['POST'] )
def authenticated(path):
    """Gestion des requêtes POST avec mTLS nécessaire
    """
    global database

    postKey = list(request.form.keys())[0]
    logging.debug( f'Méthode POST utilisée avec les données {postKey}' )
    if postKey in database.servers.keys():
        database.switchServerState(postKey)

    return render_template('pages/main.html',
                           path=path,
                           database=database,
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
            for key in data.keys():
                if key != 'save-conf' \
                and data[key] != database.config[key]:
                    logging.info( f"Enregistrement de la clé de configuration {key}" )
                    logging.debug( f"à la valeur {data[key]} en remplacement de {database.config[key]}" )
                    database.config[key] = data[key]
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

        elif 'save-serv' in data.keys():
            serverId = data['id']
            if data['current'] != data['id']:
                if data['id'] in database.servers.keys():
                    message = f"Impossible de changer le serveur de '{data['current']}'.</br>Le nom '{serverId}' est déjà attribué."
                    serverId = data['current']
                else:
                    logging.info( f"Déplacement du serveur {data['current']} vers {serverId}" )
                    database.newServer(
                        serverId=serverId,
                        server=database.delServer( serverId=data['current'] )
                    )
            if database.servers[serverId].name != data['name']:
                logging.debug( f"Mise à jour de {database.servers[serverId].name} en {data['name']}" )
                database.servers[serverId].name = data['name']
            if database.servers[serverId].faIcon != data['faIcon']:
                logging.debug( f"Mise à jour de {database.servers[serverId].faIcon} en {data['faIcon']}" )
                database.servers[serverId].faIcon = data['faIcon']
            if database.servers[serverId].daemon != data['daemon']:
                logging.debug( f"Mise à jour de {database.servers[serverId].daemon} en {data['daemon']}" )
                database.servers[serverId].daemon = data['daemon']
            database.save()

        elif 'delete-serv' in data.keys():
            database.delServer( serverId=data['current'] )

        elif 'new-serv' in data.keys():
            if data['id'] in database.servers.keys():
                message = f"Impossible de créer le serveur.</br>L'identifiant '{data['id']}' est déjà utilisé."
            else:
                logging.info( f"Création du serveur '{data['id']}'" )
                logging.debug( f"avec les valeurs '{data['name']}', '{data['faIcon']}', '{data['daemon']}'" )
                database.newServer(
                    serverId=data['id'],
                    server=Server( {
                        'name': data['name'],
                        'faIcon': data['faIcon'],
                        'daemon': data['daemon'],
                    } )
                )

    return render_template('pages/edit.html',
                           path=path,
                           database=database,
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
    
