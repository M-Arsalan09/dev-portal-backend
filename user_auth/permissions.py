from rest_framework import permissions


class RoleBasedPermission(permissions.BasePermission):
    """
    Custom permission class for role-based access control.
    - Admin users can do everything (GET, POST, PUT, PATCH, DELETE)
    - Developer users can only use GET endpoints and AI features
    """
    
    def has_permission(self, request, view):
        # Check if user is authenticated
        if not request.user or not hasattr(request.user, 'role'):
            return False
        
        user_role = request.user.role
        
        # Admin users can do everything
        if user_role == 'admin':
            return True
        
        # Developer users can only use GET methods and AI features
        if user_role == 'developer':
            # Allow GET requests
            if request.method in permissions.SAFE_METHODS:
                return True
            
            # Allow AI features (agent endpoints) - check URL path
            if request.path.startswith('/agent/'):
                return True
            
            # Allow AI features (agent endpoints) - check view action
            if hasattr(view, 'action') and view.action in ['query_gemini', 'analyze_project']:
                return True
            
            # Allow AI features for function-based views
            if hasattr(view, 'view_class') and hasattr(view.view_class, '__name__') and view.view_class.__name__ in ['query_gemini', 'analyze_project']:
                return True
            
            # Allow AI features for function-based views (alternative check)
            if hasattr(view, 'func') and hasattr(view.func, '__name__') and view.func.__name__ in ['query_gemini', 'analyze_project']:
                return True
            
            # Deny all other methods (POST, PUT, PATCH, DELETE)
            return False
        
        # Deny access for any other roles
        return False
