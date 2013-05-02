from celery.task import Task
from celery.task import periodic_task
from celery.exceptions import MaxRetriesExceededError
from celery.schedules import crontab
from datetime import timedelta, datetime
from mongoengine import *
from potter.db import make_connection
from potter.libs import notification as notification_service
from dateutil.relativedelta import relativedelta

import logging

log = logging.getLogger(__name__)

class TestTask(Task):
    def run(self, name):
	make_connection.configure()
	name = name if name else 'Siddharth'
	log.info('name: %s' %(name))

class TransactionSuccessfulEmailTask(Task):
    # Send Email to the person on payment successful 
    def run(self, tid):
	try:
	    make_connection.configure() # Making the DB connection
	    from potter.services import stripe_service as stripe_service
	    from potter.services import form as form_service
	    from potter.services import user as user_service
	    t = stripe_service.get_transaction(id = tid).to_dict()
	    f = form_service.get_form(id = t.get('form_id')).to_dict()
	    u = user_service.get_user(id = f.get('user_id')).to_dict()
	    sender_name = u.get('business_name') if u.get('business_name') else \
		    (u.get('name') if u.get('name') else u.get('email'))
	    data = {
		    't' : t,
		    'f' : f,
		    'u' : u,
		    'sender_name' : sender_name
		    }
	    sender_name = u.get('business_name') if u.get('business_name') else \
		    (u.get('name') if u.get('name') else u.get('email'))
	    bcc = u.get('email') if f.get('bcc_email') else None
	    notification_service.notify(type = 'on_payment_successful', to = t.get('email'), sender_name = sender_name,
		    data = data, cc = None, bcc = bcc)
	except Exception as e:
	    log.exception('exception while sending email. e: %s' %(e))
