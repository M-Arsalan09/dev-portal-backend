import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import UserAuth


class CustomTokenAuthentication(BaseAuthentication):
    """
    Custom token authentication that stores user role and email in the token.
    Token has no expiration for simplicity.
    """
    
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
            
        token = auth_header.split(' ')[1]
        
        try:
            # Decode the token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            # Extract user information from token
            email = payload.get('email')
            role = payload.get('role')
            
            if not email or not role:
                raise AuthenticationFailed('Invalid token payload')
            
            # Get user from database
            try:
                user = UserAuth.objects.get(email=email)
                return (user, token)
            except UserAuth.DoesNotExist:
                raise AuthenticationFailed('User not found')
                
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
    
    def authenticate_header(self, request):
        return 'Bearer'


def generate_token(user):
    """
    Generate a token for the given user with role and email.
    Token has no expiration for simplicity.
    """
    payload = {
        'email': user.email,
        'role': user.role,
        'user_id': user.id
    }
    
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token
