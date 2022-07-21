import re

from django.core.exceptions import ValidationError

def email_check(value):
    if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
        raise ValidationError("EMAIL_ERROR")

def password_check(value):
    if not re.match('^(?=.*[a-zA-z])(?=.*[0-9])(?=.*[$`~!@$!%*#^?&\\(\\)\-_=+]).{8,16}$', value):
        raise ValidationError("PASSWORD_ERROR")