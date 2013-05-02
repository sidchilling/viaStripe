from potter.conf import configuration
from potter.services import email_ses as email_ses_service
import mako.template
from mako.template import Template
from mako.lookup import TemplateLookup
import logging
import compiler

log = logging.getLogger(__name__)

def _readConfigSafe(config_text):
    ast = compiler.parse(config_text)
    d = dict()
    for x in ast.asList()[1].asList():
        name = x.asList()[0].name
        if hasattr(x.asList()[1], "value"): value = x.asList()[1].value
        else: value = [n.value for n in x.asList()[1].nodes]
        d[name] = value
    return d

def _renderer(type, data):
    lookup = TemplateLookup(directories = [configuration.email_template_directory], 
	    module_directory = configuration.email_template_cache,
	    output_encoding = 'utf-8', input_encoding = 'utf-8')
    template = lookup.get_template(configuration.email_template_map.get(type))
    data = dict((str(k), v) for k, v in data.items())
    return template.render(**data)

def _construct_notification(type, to, sender_name, data, cc, bcc):
    notification = _renderer(type = type, data = data)
    d = _readConfigSafe(notification)
    return [locals().get(var) or d.get(var) for var in ('sender', 'to', 'reply_to', 'subject', 'content')]

def notify(type, to, sender_name, data, cc, bcc):
    log.info('type: %s, to: %s, sender_name: %s, data: %s, cc: %s, bcc: %s' \
	    %(type, to, sender_name, data, cc, bcc))
    if configuration.notification_enabled:
	sender, to, reply_to, subject, content = _construct_notification(type = type,
		to = to, sender_name = sender_name, data = data,
		cc = cc, bcc = bcc)
	sender = (sender_name, configuration.email)
	return _send_email(sender = sender, to = to, reply_to = reply_to, 
		cc = cc, bcc = bcc, subject = subject, content = content, 
		type = type)

def _transform_email_field(inp):
    if isinstance(inp, tuple):
	return ["%s<%s>" % (inp[0], inp[1])]
    elif isinstance(inp, list):
	return [_transform_email_field(x) for x in inp] 
    elif inp.find(",") > 0:
	return inp.split(',')
    else:
	return [inp]

def _send_email(sender, to, reply_to, cc, bcc, subject, content, type = None, content_type = 'html'):
    assert len(to) > 0, "No To addresses."
    sender = sender[0] + "<" + sender[1] + ">" if isinstance(sender, tuple) else str(sender)
    to = _transform_email_field(to)
    bcc = _transform_email_field(bcc) if bcc else []
    cc = _transform_email_field(cc) if cc else []
    email_ses_service.send_email(sender, subject, content, to, cc, bcc, content_type)
