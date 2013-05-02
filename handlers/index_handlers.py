from brubeck.templating import MakoRendering
from brubeck.request_handling import WebMessageHandler
from brubeck.auth import web_authenticated
from user_mixin import CustomUserMixin
from json_templating import JSONRendering

from potter.services import user as user_service
from potter.services import stripe_service as stripe_service
from potter.services import form as form_service
from potter.conf import configuration

import logging
import json

log = logging.getLogger(__name__)

ERROR_MISSING_PARAMS = 'error_missing_params'

class PingHandler(JSONRendering):
    def get(self):
        resp = {'success' : 'Pong'}
        self.set_body(resp)
        return self.render()

class IndexHandler(MakoRendering, CustomUserMixin):
    def get(self):
	context = {
		'stripe_connect_url' : stripe_service.get_connect_url(),
		'username' : None
		  }
	return self.render_template('index.html', **context)

class StripeRedirectHandler(MakoRendering, CustomUserMixin):
    def get(self):
	scope = self.get_argument('scope')
	try:
	    if not self.get_argument('state', None):
		user_id = user_service.login(code = self.get_argument('code'))
		if user_id:
		    # set cookie
		    self.set_cookie(configuration.user_id_cookie_name, user_id)
		    return self.redirect('/')
		else:
		    self.set_body('some error in making new user')
		    return self.render()
	    else:
		user_service.save_test_tokens(code = self.get_argument('code'), 
			form_id = self.get_argument('state'))
		return self.redirect('/form_conf?id=%s' %(self.get_argument('state')))
	except Exception as e:
	    self.set_body('Exception: %s' %(e))
	    return self.render()

class DashboardHandler(MakoRendering, CustomUserMixin):
    @web_authenticated
    def get(self):
	log.info('user_id: %s, username: %s' %(self.current_user, self.username))
	u = user_service.get_user(id = self.current_user).to_dict()
	context = {
		'name' : u.get('name', None) if u.get('name', None) else '',
		'business_name' : u.get('business_name', None) if u.get('business_name', None) else '',
		'terms_url' : u.get('terms_url', None) if u.get('terms_url', None) else '',
		'username' : self.username,
		'show_user_details' : False,
		'forms_present' : form_service.form_present(user_id = self.current_user)
		  }
	if not u.get('name', None) or not u.get('business_name', None):
	    context['show_user_details'] = True
	else:
	    context['forms'] = form_service.get_forms(user_id = self.current_user)
	return self.render_template('dashboard.html', **context)

class CheckTestModeAllowedHandler(JSONRendering, CustomUserMixin):
    @web_authenticated
    def post(self):
	resp = {}
	try:
	    u = user_service.get_user(id = self.current_user).to_dict()
	    if not u.get('test_access_token'):
		resp['not_allowed'] = True
		resp['test_stripe_connect_url'] = stripe_service.get_test_connect_url(form_id = \
			self.get_argument('form_id'))
	    resp['success'] = True
	except Exception as e:
	    log.exception('exception while checking test mode. e: %s' %(e))
	    resp['error'] = '%s' %(e)
	self.set_body(resp)
	return self.render()

class FormConfHandler(MakoRendering, CustomUserMixin):
    @web_authenticated
    def get(self):
	form_id = self.get_argument('id')
	u = user_service.get_user(id = self.current_user).to_dict()
	f = form_service.get_form(id = form_id).to_dict()
	if u and f:
	    context = {
		    'f' : f,
		    'name' : u.get('name', None) if u.get('name', None) else '',
		    'username' : self.username,
		      }
	    return self.render_template('form_conf.html', **context)

class SaveUserDetailsHandler(JSONRendering, CustomUserMixin):
    @web_authenticated
    def post(self):
	resp = {}
	try:
	    name = self.get_argument('name').strip() if self.get_argument('name', None) \
		    else None
	    business_name = self.get_argument('business_name').strip() if self.get_argument('business_name', None) \
		    else None
	    terms_url = self.get_argument('terms_url').strip() if self.get_argument('terms_url', None) \
		    else None
	    kwargs = {
		    'set__name' : name,
		    'set__business_name' : business_name,
		    'set__terms_url' : terms_url
		     }
	    if user_service.save_details(user_id = self.current_user, **kwargs):
		resp['success'] = True
	    else:
		resp['error'] = 'error_saving'
	except Exception as e:
	    resp['error'] = '%s' %(e)
	self.set_body(resp)
	return self.render()

class NewFormHandler(JSONRendering, CustomUserMixin):
    @web_authenticated
    def post(self):
	resp = {}
	try:
	    name = self.get_argument('name').strip() if self.get_argument('name', None) \
		    else None
	    user = user_service.get_user(id = self.current_user)
	    if not name or not user:
		resp['error'] = ERROR_MISSING_PARAMS
	    else:
		kwargs = {
			'name' : name,
			'user_id' : self.current_user,
			'seller_name' : user_service.get_user_nav_name(id = self.current_user),
			'seller_email' : user.to_dict().get('email', None),
			'livemode' : True
			 }
		resp['id'] = form_service.save_new_form(**kwargs)
		resp['success'] = True
	except Exception as e:
	    resp['error'] = '%s' %(e)
	self.set_body(resp)
	return self.render()

class SaveFormConfHandler(JSONRendering, CustomUserMixin):
    @web_authenticated
    def post(self):
	resp = {}
	try:
	    id = self.get_argument('id', None)
	    if not id:
		resp['error'] = ERROR_MISSING_PARAMS
	    else:
		kwargs = {
			'set__cost' : float('%0.2f' %(float(self.get_argument('cost', 0)))),
			'set__seller_name' : self.get_argument('seller_name', None),
			'set__seller_email' : self.get_argument('seller_email', None),
			'set__description' : self.get_argument('description', None),
			'set__billing_address_required' : True if self.get_argument('billing_address_required', None) \
				else False,
			'set__send_payment_receipts' : True if self.get_argument('send_payment_receipts', None) \
				else False,
			'set__bcc_email' : True if self.get_argument('bcc_email', None) else False,
			'set__livemode' : True if self.get_argument('livemode', None) else  False
			 }
		# allow livemode to be made false only if test_access_token is present
		u = user_service.get_user(id = self.current_user).to_dict()
		if not u.get('test_access_token'):
		    kwargs['set__livemode'] = True
		form_service.update_form(id, **kwargs)
		resp['success'] = True
	except Exception as e:
	    resp['error'] = '%s' %(e)
	self.set_body(resp)
	return self.render()

class DeleteFormHandler(JSONRendering, CustomUserMixin):
    @web_authenticated
    def post(self):
	resp = {}
	try:
	    if not self.get_argument('id', None):
		raise Exception(ERROR_MISSING_PARAMS)
	    kwargs = {
		    'id' : self.get_argument('id')
		     }
	    form_service.delete_form(**kwargs)
	    resp['success'] = True
	except Exception as e:
	    resp['error'] = '%s' %(e)
	self.set_body(resp)
	return self.render()
