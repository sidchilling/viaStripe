from potter.db import *
from potter.conf import configuration as conf

import logging

log = logging.getLogger(__name__)

def form_present(user_id):
    return True if Form.objects(user_id = user_id).count() > 0 else False

def save_new_form(**kwargs):
    f = Form(**kwargs)
    f.save()
    update_kwargs = {
	    'set__url' : '%s/payment_form?id=%s' %(conf.domain, f.id)
	            }
    update_form(str(f.id), **update_kwargs)
    return '%s' %(f.id)

def get_forms(user_id):
    forms = []
    for f in Form.objects(user_id = user_id).order_by('-creation_time'):
	forms.append(f.to_dict())
    return forms

def get_form(id):
    try:
	return Form.objects(id = id).get()
    except:
	return None

def update_form(id, **kwargs):
    Form.objects(id = id).update_one(**kwargs)

def delete_form(**kwargs):
    Form.objects(**kwargs).delete()
