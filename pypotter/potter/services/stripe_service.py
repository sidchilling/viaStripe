# This contains functions for stripe

from potter.conf import configuration
from potter.db import *

import requests
import json
import logging

log = logging.getLogger(__name__)

TRANSACTION_PROCESSING = 'processing'
TRANSACTION_SUCCESS = 'success'
TRANSACTION_FAILURE = 'failure'

def get_transaction_report(form_id):
    return [t.to_dict() for t in Transaction.objects(livemode = True, 
	transaction_state = TRANSACTION_SUCCESS, form_id = form_id).order_by('-created_at')] + \
		[t.to_dict() for t in Transaction.objects(livemode = False,
		    transaction_state = TRANSACTION_SUCCESS, form_id = form_id).order_by('-created_at')]

def get_transaction(id):
    return Transaction.objects(id = id).get()

def get_connect_url():
    return 'https://connect.stripe.com/oauth/authorize?response_type=code&client_id=%s&scope=admin&stripe_landing=login' %(configuration.live_stripe_client_id)

def get_test_connect_url(form_id):
    return 'https://connect.stripe.com/oauth/authorize?response_type=code&client_id=%s&scope=admin&state=%s&stripe_landing=login' %(configuration.test_stripe_client_id, form_id)

def _get_access_token_info(code):
    r = requests.post(url = 'https://connect.stripe.com/oauth/token',
	    headers = {
		'Authorization' : 'Bearer %s' %(configuration.live_stripe_secret_key)
		},
	    data = {
		'code' : code,
		'grant_type' : 'authorization_code'
		})
    if r.ok:
	return json.loads(r.content)
    else:
	raise Exception

def _get_test_access_token_info(code):
    r = requests.post(url = 'https://connect.stripe.com/oauth/token',
	    headers = {
		'Authorization' : 'Bearer %s' %(configuration.test_stripe_secret_key)
		},
	    data = {
		'code' : code,
		'grant_type' : 'authorization_code'
		})
    if r.ok:
	return json.loads(r.content)
    else:
	raise Exception

def _get_user_info(access_token):
    r = requests.get(url = 'https://api.stripe.com/v1/account',
	    auth = (access_token, ''))
    if r.ok:
	return json.loads(r.content)
    else:
	raise Exception

def get_info(code):
    assert code, 'missing args'
    access_token_info = _get_access_token_info(code = code)
    user_info = _get_user_info(access_token = access_token_info.get('access_token', None))
    return {
	    'access_token' : access_token_info.get('access_token', None),
	    'token_type' : access_token_info.get('token_type', None),
	    'scope' : access_token_info.get('scope', None),
	    'refresh_token' : access_token_info.get('refresh_token', None),
	    'stripe_user_id' : access_token_info.get('stripe_user_id', None),
	    'stripe_publishable_key' : access_token_info.get('stripe_publishable_key', None),
	    'livemode' : access_token_info.get('livemode', None),
	    'email' : user_info.get('email', None),
	    'statement_descriptor' : user_info.get('statement_descriptor', None),
	    'details_submitted' : user_info.get('details_submitted', None),
	    'object' : user_info.get('object', None),
	    'charge_enabled' : user_info.get('charge_enabled', None),
	    'currencies' : user_info.get('currencies_supported', None)
	   }

def get_test_info(code):
    access_token_info = _get_test_access_token_info(code = code)
    log.info('access_token_info: %s' %(access_token_info))
    return {
	    'access_token' : access_token_info.get('access_token', None),
	    'token_type' : access_token_info.get('token_type', None),
	    'scope' : access_token_info.get('scope', None),
	    'refresh_token' : access_token_info.get('refresh_token', None),
	    'stripe_publishable_key' : access_token_info.get('stripe_publishable_key', None)
	   }

def _start_transaction(form_id, livemode, **kwargs):
    t = Transaction(form_id = form_id, name = kwargs.get('name_on_card', None),
	    email = kwargs.get('email', None), billing_address = kwargs.get('billing_address', None),
	    city = kwargs.get('city', None), state = kwargs.get('state', None),
	    postal_code = kwargs.get('postal_code', None), country = kwargs.get('country', None),
	    transaction_state = TRANSACTION_PROCESSING, livemode = livemode)
    t.save()
    return str(t.id)

def _charge_card(cost, token, access_token, description):
    import stripe
    stripe.api_key = access_token
    return stripe.Charge.create(amount = int(round(cost * 100)), currency = 'usd',
	    card = token, description = description)

def _mark_successful_transaction(tid, stripe_response):
    Transaction.objects(id = tid).update(set__stripe_response = stripe_response.to_dict(),
	    set__transaction_state = TRANSACTION_SUCCESS,
	    set__charge_id = stripe_response.get('id'))

def _mark_failed_transaction(tid):
    Transaction.objects(id = tid).update(set__transaction_state = TRANSACTION_FAILURE)

def make_payment(cost, form_id, token, access_token, livemode, **kwargs):
    tid = _start_transaction(form_id = form_id, livemode = livemode, **kwargs)
    try:
	stripe_response = _charge_card(cost = cost, token = token,
		access_token = access_token, description = '%s - %s' %(kwargs.get('form_name'), tid))
	_mark_successful_transaction(tid = tid, stripe_response = stripe_response)
	return tid
    except Exception as e:
	log.exception('exception occurrred while charging the card. e: %s' %(e))
	_mark_failed_transaction(tid = tid)
	return None

