import logging

from potter.services import stripe_service as stripe_service
from potter.services import form as form_service
from potter.db import *

log = logging.getLogger(__name__)

def get_user(**kwargs):
    try:
	return User.objects(**kwargs).get()
    except:
	return None

def get_user_nav_name(id):
    u = get_user(id = id)
    if u:
	if u.business_name:
	    return u.business_name
	if u.name:
	    return u.name
	return u.email
    else:
	return None

def login(code):
    assert code, 'missing args'
    user_stripe_details = stripe_service.get_info(code = code)
    u = get_user(stripe_user_id = user_stripe_details.get('stripe_user_id'))
    if u:
	# Update access_token
	User.objects(id = str(u.id)).update(set__live_access_token =
		user_stripe_details.get('access_token'))
	return '%s' %(u.id)
    else:
	return _add_new_user(user_stripe_details = user_stripe_details)

def save_test_tokens(code, form_id):
    d = stripe_service.get_test_info(code = code)
    log.info('d: %s' %(d))
    f = form_service.get_form(id = form_id).to_dict()
    update_params = {
	    'set__test_access_token' : d.get('access_token', None),
	    'set__test_token_type' : d.get('token_type', None),
	    'set__test_scope' : d.get('scope', None),
	    'set__test_refresh_token' : d.get('refresh_token', None),
	    'set__test_stripe_publishable_key' : d.get('stripe_publishable_key', None)
	    }
    # For localhost, as we are same secret - update access_token
    # update_params['set__live_access_token'] = d.get('access_token', None)
    log.info('update_params: %s' %(update_params))
    User.objects(id = f.get('user_id')).update(**update_params)

def _add_new_user(user_stripe_details):
    user = User(live_access_token = user_stripe_details.get('access_token', None),
	    live_token_type = user_stripe_details.get('token_type', None),
	    live_scope = user_stripe_details.get('scope', None),
	    live_refresh_token = user_stripe_details.get('refresh_token', None),
	    stripe_user_id = user_stripe_details.get('stripe_user_id', None),
	    live_stripe_publishable_key = user_stripe_details.get('stripe_publishable_key', None),
	    livemode = user_stripe_details.get('livemode', None),
	    email = user_stripe_details.get('email', None),
	    stripe_statement_descriptor = user_stripe_details.get('statement_descriptor', None),
	    stripe_object = user_stripe_details.get('object', None),
	    stripe_details_submitted = user_stripe_details.get('details_submitted', None),
	    stripe_charge_enabled = user_stripe_details.get('charge_enabled', None),
	    stripe_currencies = user_stripe_details.get('currencies', None))
    user.save()
    return '%s' %(user.id)

def save_details(user_id, **kwargs):
    User.objects(id = user_id).update(**kwargs)
    return True
