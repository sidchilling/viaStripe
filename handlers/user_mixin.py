from brubeck.auth import UserHandlingMixin
import logging

from potter.conf import configuration
from potter.services import user as user_service

log = logging.getLogger(__name__)

class CustomUserMixin(UserHandlingMixin):
    def get_current_user(self):
	# The user_id returned from here will be set in self.current_user
	user_id = self.get_cookie(configuration.user_id_cookie_name)
	if not user_id:
	    log.error('Auth Fail: No user_id found in cookie')
	    return
	self.username = user_service.get_user_nav_name(id = user_id)
	return user_id

