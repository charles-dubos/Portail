import sys, logging

sys.path.insert(0,"/var/www/html")

from monSite import create_app
application = create_app()
