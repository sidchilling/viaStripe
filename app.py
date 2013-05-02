from brubeck.request_handling import Brubeck, WebMessageHandler
from brubeck.connections import Mongrel2Connection
from brubeck.templating import MakoRendering, load_mako_env
import sys

from handlers import index_handlers
from handlers import payment_handlers
from potter.db import make_connection as db_connection_service

# Connect to database before every request
db_connection_service.configure()

routes = [
	(r'^/stripe_redirect', index_handlers.StripeRedirectHandler),
	(r'^/submit_payment_with_address', payment_handlers.PayAddressHandler),
	(r'^/submit_payment_without_address', payment_handlers.PayHandler),
	(r'^/login', index_handlers.IndexHandler),
	(r'^/check_test_mode_allowed', index_handlers.CheckTestModeAllowedHandler),
	(r'^/save_user_details', index_handlers.SaveUserDetailsHandler),
	(r'^/get_form_transactions', payment_handlers.GetFormTransactionsHandler),
	(r'^/save_new_form', index_handlers.NewFormHandler),
	(r'^/form_conf', index_handlers.FormConfHandler),
	(r'^/save_form_conf', index_handlers.SaveFormConfHandler),
	(r'^/form_delete', index_handlers.DeleteFormHandler),
	(r'^/payment_form', payment_handlers.PaymentFormHandler),
	(r'^/ping', index_handlers.PingHandler),
	(r'^/', index_handlers.DashboardHandler)
	 ]

config = {
	'msg_conn' : Mongrel2Connection('tcp://127.0.0.1:9999', 'tcp://127.0.0.1:9998'),
	'handler_tuples' : routes,
	'template_loader' : load_mako_env('./templates'),
	'login_url' : '/login' # This is the URL the user will be redirected to when not logged in
	 }

app = Brubeck(**config)
app.run()
