from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .services import GeminiService
from user_auth.authentication import CustomTokenAuthentication
from user_auth.permissions import RoleBasedPermission
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([permissions.AllowAny])
def query_gemini(request):
    """
    API endpoint to send queries to Gemini and return responses
    
    Expected request body:
    {
        "query": "Your question or prompt here"
    }
    
    Returns:
    {
        "success": true/false,
        "response": "Gemini's response text",
        "model": "gemini-2.5-flash",
        "error": "Error message if any"
    }
    """
    try:
        # Get query from request body
        query = request.data.get('query')
        
        if not query:
            return Response({
                "success": False,
                "error": "Query is required in request body",
                "model": "gemini-2.5-flash"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Initialize Gemini service and generate content
        gemini_service = GeminiService()
        result = gemini_service.generate_content(query)
        
        # Return appropriate response based on success/failure
        if result["success"]:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Unexpected error in query_gemini view: {str(e)}")
        return Response({
            "success": False,
            "error": f"Internal server error: {str(e)}",
            "model": "gemini-2.5-flash"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([permissions.AllowAny])
def analyze_project(request):
    """
    API endpoint to analyze project requirements and suggest suitable developers
    
    Expected request body (multipart/form-data):
    - project_name (required): Name of the project
    - project_description (optional): Text description of the project
    - project_file (optional): PDF or DOCX file containing project description
    - required_skills (optional): JSON string array of required skills
    - project_categories (optional): JSON string array of project categories
    
    Note: Either project_description or project_file must be provided
    
    Returns:
    {
        "success": true/false,
        "project_name": "Project Name",
        "project_description": "Project description",
        "required_skills": ["Python", "Django"],
        "project_categories": ["Web Development"],
        "total_developers_analyzed": 5,
        "analysis": "Detailed analysis and recommendations from Gemini",
        "model": "gemini-2.5-flash",
        "error": "Error message if any"
    }
    """
    try:
        # Get project details from request
        project_name = request.data.get('project_name')
        project_description = request.data.get('project_description')
        project_file = request.FILES.get('project_file')
        required_skills = request.data.get('required_skills', [])
        project_categories = request.data.get('project_categories', [])
        
        # Parse JSON strings if they exist
        if isinstance(required_skills, str):
            try:
                import json
                required_skills = json.loads(required_skills)
            except json.JSONDecodeError:
                required_skills = []
        
        if isinstance(project_categories, str):
            try:
                import json
                project_categories = json.loads(project_categories)
            except json.JSONDecodeError:
                project_categories = []
        
        # Validate required fields
        if not project_name:
            return Response({
                "success": False,
                "error": "project_name is required",
                "model": "gemini-2.5-flash"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate that either description or file is provided
        if not project_description and not project_file:
            return Response({
                "success": False,
                "error": "Either project_description or project_file must be provided",
                "model": "gemini-2.5-flash"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Initialize Gemini service and analyze project
        gemini_service = GeminiService()
        result = gemini_service.analyze_project_and_suggest_developers(
            project_name=project_name,
            project_description=project_description,
            project_file=project_file,
            required_skills=required_skills if required_skills else None,
            project_categories=project_categories if project_categories else None
        )
        
        # Return appropriate response based on success/failure
        if result["success"]:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Unexpected error in analyze_project view: {str(e)}")
        return Response({
            "success": False,
            "error": f"Internal server error: {str(e)}",
            "model": "gemini-2.5-flash"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
