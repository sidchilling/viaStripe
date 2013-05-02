from mongoengine import *
from datetime import datetime

import logging

class User(Document):
    live_access_token = StringField(required = True)
    live_token_type = StringField(default = None)
    live_scope = StringField(default = None)
    live_refresh_token = StringField(default = None)
    test_access_token = StringField(default = None)
    test_token_type = StringField(default = None)
    test_scope = StringField(default = None)
    test_refresh_token = StringField(default = None)
    stripe_user_id = StringField(default = None)
    live_stripe_publishable_key = StringField(required = True)
    test_stripe_publishable_key = StringField(default = None)
    livemode = BooleanField(default = False)
    email = StringField(default = None)
    stripe_statement_descriptor = StringField(default = None)
    stripe_details_submitted = BooleanField(default = None)
    stripe_object = StringField(default = None)
    stripe_charge_enabled = BooleanField(default = None)
    stripe_currencies = ListField(StringField(), default = [])
    name = StringField(default = None)
    business_name = StringField(default = None)
    logo_url = StringField(default = None)
    terms_url = StringField(default = None)
    creation_time = DateTimeField(default = datetime.utcnow)

    meta = {
	    'indexes' : ['live_access_token', 'test_access_token', 'stripe_user_id', 'email', 'name', 'business_name']
	   }

    def to_dict(self):
	return {
		'id' : str(self.id),
		'live_access_token' : self.live_access_token,
		'live_token_type' : self.live_token_type,
		'live_scope' : self.live_scope,
		'live_refresh_token' : self.live_refresh_token,
		'test_access_token' : self.test_access_token,
		'test_token_type' : self.test_token_type,
		'test_scope' : self.test_scope,
		'test_refresh_token' : self.test_refresh_token,
		'stripe_user_id' : self.stripe_user_id,
		'live_stripe_publishable_key' : self.live_stripe_publishable_key,
		'test_stripe_publishable_key' : self.test_stripe_publishable_key,
		'livemode' : self.livemode,
		'email' : self.email,
		'stripe_statement_descriptor' : self.stripe_statement_descriptor,
		'stripe_details_submitted' : self.stripe_details_submitted,
		'stripe_object' : self.stripe_object,
		'stripe_charge_enabled' : self.stripe_charge_enabled,
		'stripe_currencies' : self.stripe_currencies,
		'name' : self.name,
		'business_name' : self.business_name,
		'logo_url' : self.logo_url,
		'terms_url' : self.terms_url
	       }

class Form(Document):
    name = StringField(required = True)
    user_id = StringField(required = True)
    creation_time = DateTimeField(default = datetime.utcnow)
    livemode = BooleanField(default = False)
    description = StringField(default = None)
    url = StringField(default = None)
    cost = FloatField(default = 0)
    billing_address_required = BooleanField(default = False)
    send_payment_receipts = BooleanField(default = False)
    bcc_email = BooleanField(default = True)
    seller_name = StringField(default = None)
    seller_email = StringField(default = None)

    meta = {
	    'indexes' : ['name']
	   }

    def to_dict(self):
	return {
		'id' : str(self.id),
		'user_id' : self.user_id,
		'name' : self.name,
		'livemode' : self.livemode,
		'description' : self.description if self.description else '',
		'url' : self.url,
		'creation_time' : self.creation_time.strftime('%b %d, %Y'),
		'cost' : '%0.2f' %(self.cost),
		'billing_address_required' : self.billing_address_required,
		'send_invoice_email' : self.send_payment_receipts,
		'bcc_email' : self.bcc_email,
		'seller_name' : self.seller_name,
		'seller_email' : self.seller_email
	       }

class Transaction(Document):
    form_id = StringField(required = True)
    name = StringField(required = True)
    email = StringField(required = True)
    billing_address = StringField(default = None)
    city = StringField(default = None)
    state = StringField(default = None)
    postal_code = StringField(default = None)
    country = StringField(default = None)
    transaction_state = StringField(default = None)
    charge_id = StringField(default = None)
    stripe_response = StringField(default = None)
    livemode = BooleanField(default = None)
    created_at = DateTimeField(default = datetime.utcnow)

    meta = {
	    'indexes' : ['form_id', 'email', 'name', 'charge_id']
	   }

    def to_dict(self):
	return {
		'id' : str(self.id),
		'form_id' : self.form_id,
		'name' : self.name,
		'email' : self.email,
		'billing_address' : self.billing_address,
		'city' : self.city,
		'state' : self.state,
		'postal_code' : self.postal_code,
		'country' : self.country,
		'transaction_state' : self.transaction_state,
		'charge_id' : self.charge_id,
		'stripe_response' : self.stripe_response,
		'livemode' : self.livemode,
		'created_at' : self.created_at.strftime('%Y-%m-%d %H:%M')
	       }
