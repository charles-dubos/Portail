from flask import Blueprint, redirect, render_template, request, url_for
from monSite.functions.general import *

# BLUEPRINTS
bp=Blueprint("pages", __name__)


@bp.route('/')
def index():
    """Page principale -> redirection vers la page paramétrée
    """
    logging.info('Redirection vers "{}"'.format(
        Database(DATABASE_NAME).config['mainPage']
    ))
    
    return redirect(Database(DATABASE_NAME).config['mainPage'])


@bp.route( '/<path>', methods=['GET','POST'] )
def main(path):
    """Page par identifiant de famille
    """
    global database

    if request.method == 'POST':
        postKey = list(request.form.keys())[0]
        logging.debug( f'Méthode POST utilisée avec les données {postKey}' )
        if postKey in database.servers.keys():
            database.servers[postKey].switchState()

    return render_template('pages/main.html',
                           path=path,
                           database=database,
                           previous=prevPage( database=database, current=path ),
                           next=nextPage( database=database, current=path ),
                           ratio=1
                           )


@bp.route( '/<path>/edit', methods=['GET','POST'] )
def edit(path):
    """Page d'édition par identifiant de famille
    """
    global database

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
                    return 
                    # TODO: retour popup erreur carte existante
                else:
                    deleteCard(
                        database=database,
                        familyId=path,
                        cardId=data['current']
                    )
                editCard(
                    database=database,
                    familyId=path,
                    cardId=data['number'],
                    data=data
                )
                database.save()
                
        elif 'new-card' in data.keys():
            if data['number'] in database.families[path].dictOfCards.keys():
                return
                # TODO: retour popup erreur carte existante
            editCard(
                database=database,
                familyId=path,
                cardId=data['number'],
                data=data
            )
            database.save()

        elif 'save-conf' in data.keys():
            for key in data.keys():
                if key != 'save-conf' \
                    and data[key] != database.config[key]:
                    logging.info( f"Enregistrement de la clé de configuration {key}" )
                    logging.debug( f"à la valeur {data[key]} en remplacement de {database.config[key]}" )
                    database.config[key]=data[key]
                    database.save()

        elif 'save-fam' in data.keys():
            if data['current'] != data['famId']:
                if data['famId'] in database.families.keys():
                    return 
                    # TODO: retour popup erreur famille existante
                logging.info( f"Déplacement de la famille {path} vers {data['famId']}" )
                database.newFamily(
                    familyId=data['famId'],
                    family=database.delFamily( familyId=data['current'] )
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
                return
                # ToDO popup erreur base minimaliste
            path=nextPage( database=database, current=path )
            database.delFamily( data['current'] )

        elif 'new-fam' in data.keys():
            if data['famId'] in database.families.keys():
                return 
                # TODO: retour popup erreur famille existante
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
            database.save()
            path = data['famId']

        elif 'save-serv' in data.keys():
            if data['current'] != data['id']:
                if data['id'] in database.servers.keys():
                    return 
                    # TODO: retour popup erreur serveur existant
                logging.info( f"Déplacement du serveur {data['current']} vers {data['id']}" )
                database.newServer(
                    serverId=data['id'],
                    server=database.delServer( serverId=data['current'] )
                )
            serverId = data['id']
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
                return 
                # TODO: retour popup erreur serveur existant
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
            database.save()

    return render_template('pages/edit.html',
                           path=path,
                           database=database,
                           previous=prevPage(database=database, current=path),
                           next=nextPage(database=database, current=path),
                           ratio=1,
                           newNumber=firstAvailable(database=database, current=path)
                           )
