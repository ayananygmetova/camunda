"""
Token recognition occurs in this file.
"""
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

def get_token(user):
    """
    Return token by JWT authentication.
    :param user:
    :return: current user token
    """
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    refresh = RefreshToken.for_user(user)
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }
