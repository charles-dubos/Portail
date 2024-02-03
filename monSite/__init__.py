from flask import Flask
from monSite import pages
from monSite.functions.general import *
# python -m flask --app monSite run --port 8000 --debug

def create_app():

    app = Flask(__name__)

    app.register_blueprint(pages.bp)
    return app
