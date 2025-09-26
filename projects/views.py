from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from developers.models import Skills
from .models import ProjectCategory, ProjectCategorySkills
from .serializers import ProjectCategorySerializer, ProjectCategorySkillsSerializer, ProjectCategoryListSerializer
from user_auth.authentication import CustomTokenAuthentication
from user_auth.permissions import RoleBasedPermission


class ProjectCategoryViewSet(viewsets.ViewSet):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [RoleBasedPermission]
    
    def list(self, request):
        project_categories = ProjectCategory.objects.all()
        #paginate the project categories
        paginator = PageNumberPagination()
        paginator.page_size = 10
        if project_categories and project_categories.count() > 0:
            paginated_project_categories = paginator.paginate_queryset(project_categories, request)
            serializer = ProjectCategoryListSerializer(paginated_project_categories, many=True)
            paginated_response = paginator.get_paginated_response(serializer.data)
            pagination_data = paginated_response.data
            count = pagination_data.get('count', 0)
            next_page = pagination_data.get('next', None)
            previous_page = pagination_data.get('previous', None)
            results = pagination_data.get('results', [])
            return Response({"details": "Project categories fetched successfully", "data": results, "pagination": {
                "count": count,
                "next": next_page,
                "previous": previous_page,
                "current_page": request.GET.get('page', 1),
                "page_size": paginator.page_size
            }}, status=status.HTTP_200_OK)
        else:
            return Response({"details": "Project categories fetched successfully", "data": [], "pagination": {
                "count": 0,
                "next": None,
                "previous": None,
                "current_page": 1,
                "page_size": paginator.page_size
            }}, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = ProjectCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"details": "Project category created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        project_category = ProjectCategory.objects.filter(id=pk).first()
        if not project_category:
            return Response({"details": "Project category not found"}, status=status.HTTP_404_NOT_FOUND)
        skills = ProjectCategorySkills.objects.filter(project_category=project_category)
        # group skills by skill area
        skill_areas_dict = {}
        for skill in skills:
            skill_area_id = skill.skill.skill_area.id
            skill_area_name = skill.skill.skill_area.name
            if skill_area_id not in skill_areas_dict:
                skill_areas_dict[skill_area_id] = {
                    "skill_area_id": skill_area_id,
                    "skill_area_name": skill_area_name,
                    "skills": []
                }
            skill_areas_dict[skill_area_id]["skills"].append({
                "skill_id": skill.skill.id,
                "skill_name": skill.skill.name
            })
        skill_dict = list(skill_areas_dict.values())
        serializer = ProjectCategorySerializer(project_category)
        data = serializer.data
        data['skills'] = skill_dict
        return Response({"details": "Project category fetched successfully", "data": data}, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        
        project_category = ProjectCategory.objects.filter(id=pk).first()
        if not project_category:
            return Response({"details": "Project category not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Handle use_cases update
        use_cases = request.data.get('use_cases', [])
        description = request.data.get('description', None)
        if use_cases:
            # If use_cases is provided, replace the existing list
            previous_use_cases = project_category.use_cases
            use_cases = previous_use_cases + use_cases
            print(use_cases)
            project_category.use_cases = use_cases
            project_category.save()
            
        if description:
            project_category.description = description
            project_category.save()
        
        if not use_cases and not description:
            return Response({"details": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProjectCategoryListSerializer(project_category)
        return Response({"details": "Project category updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            
        
        
        
    
    @action(detail=False, methods=['post'])
    def add_required_skills(self, request):
        project_category_id = request.data.get('project_category_id')
        if not project_category_id:
            return Response({"details": "Project category id is required"}, status=status.HTTP_400_BAD_REQUEST)
        project_category = ProjectCategory.objects.filter(id=project_category_id).first()
        if not project_category:
            return Response({"details": "Project category not found"}, status=status.HTTP_404_NOT_FOUND)
        skill_ids = request.data.get('skill_ids')
        if not skill_ids:
            return Response({"details": "Skill ids are required"}, status=status.HTTP_400_BAD_REQUEST)
        for skill_id in skill_ids:
            skill = Skills.objects.filter(id=skill_id).first()
            if not skill:
                print("skill not found: ", skill_id)
                continue
            skill_obj = ProjectCategorySkills.objects.filter(project_category=project_category, skill=skill).first()
            if skill_obj:
                #skill already exists
                print("skill already exists: ", skill_obj)
                continue
            else:
                #skill does not exist, create it
                ProjectCategorySkills.objects.create(project_category=project_category, skill=skill)
        return Response({"details": "Skills added successfully"}, status=status.HTTP_200_OK)
        
    
    def destroy(self, request, pk=None):
        return Response({"details": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)