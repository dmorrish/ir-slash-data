import base64
import hashlib


def encode_password(username, password):
    """ Encodes the username/password combination as a Base64 string for
    submission in the password field on iRacing login forms. This is not what
    iRacing stores as the hashed password. It is merely to prevent the plain
    text version of a user's password from being transmitted to iRacing.
    """
    s256Hash = hashlib.sha256((password + username.lower()).encode('utf-8')).digest()
    base64Hash = base64.b64encode(s256Hash).decode('utf-8')

    return base64Hash
