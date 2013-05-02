# This file contains the data of configuration items required by the application

# Stripe configuration items
test_stripe_client_id = '<your-test-stripe-client-id>'
test_stripe_secret_key = '<your-test-stripe-secret-key>'

live_stripe_client_id = '<your-live-stripe-client-id>'
live_stripe_secret_key = '<your-live-stripe-secret-key>'

# Database related configuration
db_host = 'localhost'
db_port = '27017'
db_name = 'payme_db'
db_username = None
db_password = None

# client side cookie related info
user_id_cookie_name = 'user_id_payme'

# Domain related
domain = 'http://www.viastripe.com'

# Email notifications
notification_enabled = True
email = 'noreply@shopsocially.com'
email_template_directory = '/home/ubuntu/denarit/payme/brubeck-work/templates/email/'
email_template_cache = '/tmp/email_template_cache/'
email_template_map = {
	'on_payment_successful' : 'on_payment_successful.html'
	}
aws_access_key_id = '<your-aws-access-key-id>'
aws_secret_access_key = '<your-aws-secret-access-key>'

