# This is the celery config file

BROKER_URL = 'redis://localhost:6379/1'
CELERY_BACKEND = 'amqp'
CELERY_IGNORE_RESULT = True
CELERY_MONGODB_BACKEND_SETTINGS = {
	'host' : '127.0.0.1',
	'port' : '27017',
	'database' : 'payme_db',
	'taskmeta_collection' : 'my_taskmeta_collection'
	}

# Queue Information
CELERY_QUEUES = {
	'default' : {
	    'binding_key' : 'default'
	    }
	}
CELERY_DEFAULT_QUEUE = "default"
CELERY_DEFAULT_EXCHANGE = "default"
CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_DEFAULT_ROUTING_KEY = "default"

from datetime import datetime
from celery.schedules import crontab

# Redis related settings
REDIS_SETTINGS = {
	"host" : "localhost",
	"port" : "6379",
	"database" : "1",
	}

# Redis for targeting related settings
REDIS_TARGETING_SETTINGS = {
	"host" : "localhost",
	"port" : "6379",
	"database" : "3",
	}


# Number of processes that processes tasks simultaneously.
CELERYD_CONCURRENCY = 8

# Modules to import when celeryd starts.
# This must import every module where you register tasks so celeryd
# is able to find and run them.
CELERY_IMPORTS = ('potter.tasks')

CELERY_SEND_TASK_ERROR_EMAILS = False

from mongoengine import connection

connection._connection_settings['host'] = CELERY_MONGODB_BACKEND_SETTINGS.get('host', '127.0.0.1')
connection._connection_settings['port'] = int(CELERY_MONGODB_BACKEND_SETTINGS.get('port', 27017))
connection._db_name = CELERY_MONGODB_BACKEND_SETTINGS.get('database', 'payme_db')
