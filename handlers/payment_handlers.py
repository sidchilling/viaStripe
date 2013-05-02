from brubeck.templating import MakoRendering
from brubeck.request_handling import WebMessageHandler
from brubeck.auth import web_authenticated
from json_templating import JSONRendering
from user_mixin import CustomUserMixin

from potter.services import stripe_service as stripe_service
from potter.services import form as form_service
from potter.services import user as user_service
from potter.conf import configuration
from potter.tasks import *

from datetime import datetime
import logging
import json

log = logging.getLogger(__name__)

ERROR_MISSING_PARAMS = 'All the fields are not filled'

class PaymentFormHandler(MakoRendering):
    def get(self):
	try:
	    if not self.get_argument('id', None):
		self.status_code = 404
		return self.render_template('404.html')
	    f = form_service.get_form(id = self.get_argument('id')).to_dict()
	    u = user_service.get_user(id = f.get('user_id', None)).to_dict()
	    months = [
		    {'value' : '', 'month' : ''},
		    {'value' : '01', 'month' : 'Jan'},
		    {'value' : '02', 'month' : 'Feb'},
		    {'value' : '03', 'month' : 'Mar'},
		    {'value' : '04', 'month' : 'Apr'},
		    {'value' : '05', 'month' : 'May'},
		    {'value' : '06', 'month' : 'Jun'},
		    {'value' : '07', 'month' : 'Jul'},
		    {'value' : '08', 'month' : 'Aug'},
		    {'value' : '09', 'month' : 'Sep'},
		    {'value' : '10', 'month' : 'Oct'},
		    {'value' : '11', 'month' : 'Nov'},
		    {'value' : '12', 'month' : 'Dec'}
		     ]
	    years = ['']
	    for i in range(0, 20):
		years.append(int(datetime.utcnow().strftime('%Y')) + i)
	    context = {
		    'f' : f,
		    'u' : u,
		    'months' : months,
		    'years' : years
		      }
	    return self.render_template('payment_form.html', **context)
	except Exception as e:
	    log.exception('exception: %s' %(e))
	    return self.render_template('404.html')

class PayAddressHandler(JSONRendering):
    def post(self):
	resp = {}
	try:
	    if not self.get_argument('token', None) \
		    or not self.get_argument('form_id', None) \
		    or not self.get_argument('name_on_card', None) \
		    or not self.get_argument('email', None) \
		    or not self.get_argument('billing_address', None) \
		    or not self.get_argument('city', None) \
		    or not self.get_argument('state', None) \
		    or not self.get_argument('postal_code', None) \
		    or not self.get_argument('country', None):
			resp['error'] = ERROR_MISSING_PARAMS
	    else:
		f = form_service.get_form(id = self.get_argument('form_id')).to_dict()
		u = user_service.get_user(id = f.get('user_id')).to_dict()
		kwargs = {
			'name_on_card' : self.get_argument('name_on_card', None),
			'email' : self.get_argument('email', None),
			'billing_address' : self.get_argument('billing_address', None),
			'city' : self.get_argument('city', None),
			'state' : self.get_argument('state', None),
			'postal_code' : self.get_argument('postal_code', None),
			'country' : self.get_argument('country', None),
			'form_name' : f.get('name', None)
			 }
		access_token = u.get('live_access_token') if f.get('livemode') else u.get('test_access_token')
		tid = stripe_service.make_payment(cost = float(f.get('cost')), form_id = f.get('id'),
			token = self.get_argument('token', None),
			access_token = access_token, livemode = f.get('livemode', True),
			**kwargs)
		if tid:
		    resp = {
			    'success' : True,
			    'name_on_card' : kwargs.get('name_on_card', None),
			    'email' : kwargs.get('email', None),
			    'cost' : f.get('cost'),
			    'transaction_id' : tid
			   }
		    if f.get('send_invoice_email'):
			TransactionSuccessfulEmailTask.delay(tid = tid)
		else:
		    resp['error'] = 'Could not charge card'
	except Exception as e:
	    log.exception('exception: %s' %(e))
	    resp['error'] = '%s' %(e)
	self.set_body(resp)
	return self.render()

class GetFormTransactionsHandler(JSONRendering, CustomUserMixin):
    @web_authenticated
    def post(self):
	resp = {}
	try:
	    resp = {
		    'success' : True,
		    'transactions' : stripe_service.get_transaction_report(form_id = \
			    self.get_argument('form_id', None))
		   }
	except Exception as e:
	    log.exception('Exception. e: %s' %(e))
	    resp['error'] = '%s' %(e)
	self.set_body(resp)
	return self.render()

class PayHandler(JSONRendering):
    def post(self):
	resp = {}
	try:
	    if not self.get_argument('token', None) \
		    or not self.get_argument('form_id', None) \
		    or not self.get_argument('email', None) \
		    or not self.get_argument('name_on_card', None):
			resp['error'] = ERROR_MISSING_PARAMS
	    else:
		f = form_service.get_form(id = self.get_argument('form_id')).to_dict()
		u = user_service.get_user(id = f.get('user_id')).to_dict()
		kwargs = {
			'name_on_card' : self.get_argument('name_on_card', None),
			'email' : self.get_argument('email', None),
			'form_name' : f.get('name', None)
			 }
		access_token = u.get('live_access_token') if f.get('livemode') else u.get('test_access_token')
		tid = stripe_service.make_payment(cost = float(f.get('cost')), form_id = f.get('id'),
			token = self.get_argument('token', None),
			access_token = access_token, livemode = f.get('livemode', True),
			**kwargs)
		if tid:
		    resp = {
			    'success' : True,
			    'name_on_card' : kwargs.get('name_on_card', None),
			    'email' : kwargs.get('email', None),
			    'cost' : f.get('cost'),
			    'transaction_id' : tid
			   }
		    if f.get('send_invoice_email'):
			TransactionSuccessfulEmailTask.delay(tid = tid)
		else:
		    resp['error'] = 'Could not charge card'
	except Exception as e:
	    log.exception('exception while payment. e: %s' %(e))
	    resp['error'] = '%s' %(e)
	self.set_body(resp)
	return self.render()
