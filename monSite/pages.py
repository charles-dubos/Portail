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


@bp.route('/<path>', methods=['GET','POST'])
def main(path):
    """Page par identifiant de famille
    """
    global database

    if request.method == 'POST':
        postKey=list(request.form.keys())[0]
        logging.debug(f'Méthode POST utilisée avec les données {postKey}')
        if postKey in database.servers.keys():
            database.servers[postKey].switchState()

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

    if request.method == 'POST':
        data = dict(request.form.items(multi=False))
        logging.debug(f'Méthode POST utilisée avec les données {data.keys()}')

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
                    # TODO: retour popup erreur famille existante
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
                # TODO: retour popup erreur famille existante
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
                    logging.info(f"Enregistrement de la clé de configuration {key}")
                    logging.debug(f"à la valeur {data[key]} en remplacement de {database.config[key]}")
                    database.config[key]=data[key]
                    database.save()


    return render_template('pages/edit.html',
                           path=path,
                           database=database,
                           previous=prevPage(database=database, current=path),
                           next=nextPage(database=database, current=path),
                           ratio=1,
                           newNumber=firstAvailable(database=database, current=path)
                           )
