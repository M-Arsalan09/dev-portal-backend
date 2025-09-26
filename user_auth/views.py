from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.decorators import authentication_classes, permission_classes

from .models import UserAuth
from .authentication import CustomTokenAuthentication, generate_token
from .permissions import RoleBasedPermission



class LoginView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        auth = UserAuth.objects.filter(email=email).first()
        if not auth:
            return Response({"details": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if not check_password(password, auth.password):
            return Response({"details": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(
            {
                "details": "Login successful",
                "token": generate_token(auth),
                "data": {
                    "email": auth.email,
                    "role": auth.role,
                    "first_login": auth.first_login
                }
            }, status=status.HTTP_200_OK)
    

class UpdatePasswordView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        # Get the authenticated user from the token
        user = request.user
        
        password = request.data.get('password')
        role = request.data.get('role')
        
        if not password:
            return Response({"details": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if role and role == user.role and role != "developer":
            return Response({"details": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.password = make_password(password)
        user.first_login = False
        user.save()
        
        return Response({"details": "Password updated successfully"}, status=status.HTTP_200_OK)
    
class CreateUserView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [RoleBasedPermission]
    
    def post(self, request):
        # Get the authenticated user from the token
        authenticated_user = request.user
        
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')
        
        if not email or not password:
            return Response({"details": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Only admin users can create other users
        if authenticated_user.role != "admin":
            return Response({"details": "Only admin users can create new users"}, status=status.HTTP_403_FORBIDDEN)
        
        
        auth = UserAuth.objects.filter(email=email).first()
        if auth:
            return Response({"details": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        auth = UserAuth.objects.create(email=email, password=make_password(password), role="developer")
        return Response({"details": "User created successfully"}, status=status.HTTP_201_CREATED)
        