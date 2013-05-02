from mongoengine import connect
import logging

from potter.conf import configuration

log = logging.getLogger(__name__)

def configure():
    connect(host = configuration.db_host, db = configuration.db_name)

