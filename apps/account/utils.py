import string


from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

User = get_user_model()


def generate_username():

    try:
        letters = string.ascii_letters
    except AttributeError:
        letters = string.letters

    allowed_char = letters + string.digits + '_'
    uname = get_random_string(length=30, allowed_chars=allowed_char)
    try:
        User.objects.get(username=uname)
        return generate_username()
    except User.DoesNotExist:
        return uname
