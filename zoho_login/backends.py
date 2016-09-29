from __future__ import unicode_literals
from zoho_login.compat import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from zoho_login import zoho


class ZohoApiBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
	for domain in settings.ZOHO_LOGIN_EMAIL_DOMAINS:
	    if domain in username:
		# domain matched
		try:
		    # If user already in django and password changed
		    _user = UserModel._default_manager.get_by_natural_key(username)
		    valid, user = self.is_valid_zoho_account(username, password, _user)
		    if valid:
		        return user
		except UserModel.DoesNotExist:
		    # If user not in django but in zoho
		    valid, user = self.is_valid_zoho_account(username, password)
		    if valid:
		        return user
		break

    def is_valid_zoho_account(self, username, password, uuser=None):
        details = zoho.ZohoApi(username=username, password=password).create_auth_token()
        if details['status'] == "success":
            details["username"] = username
            details["password"] = password
            user = self._create_user(details, uuser)
            return True, user
        return False, details.get("message", _('Error'))

    def _create_user(self, details, uuser):
        UserModel = get_user_model()
        user = uuser if uuser else UserModel()
        user.username = details["username"]
        user.set_password(details["password"])
        user.save()
        return user
