from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import Developers, SkillAreas, Skills, DeveloperSkills, DeveloperProjects, DeveloperSkillLevel
from .serializers import DeveloperListSerializer, DeveloperSerializer, SkillAreaSerializer, DeveloperProjectsSerializer, DeveloperProjectsListSerializer
from .services import SkillLevelService

class DeveloperViewSet(viewsets.ViewSet):
    
    def list(self, request):
        developers = Developers.objects.all()
        
        # Initialize pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set page size to 10 items per page
        
        # Paginate the queryset
        if developers and developers.count() > 0:
            paginated_developers = paginator.paginate_queryset(developers, request)
            serializer = DeveloperListSerializer(paginated_developers, many=True)
        
            # Get pagination metadata
            
            paginated_response = paginator.get_paginated_response(serializer.data)
            pagination_data = paginated_response.data
            
            # Extract pagination info separately
            count = pagination_data.get('count', 0)
            next_page = pagination_data.get('next', None)
            previous_page = pagination_data.get('previous', None)
            results = pagination_data.get('results', [])
            
            # Return custom response format
            return Response({
                "details": "Developers fetched successfully",
                "data": results,
                "pagination": {
                    "count": count,
                    "next": next_page,
                    "previous": previous_page,
                    "current_page": request.GET.get('page', 1),
                    "page_size": paginator.page_size
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "details": "Developers fetched successfully",
                "data": [],
                "pagination": {
                    "count": 0,
                    "next": None,
                    "previous": None,
                    "current_page": 1,
                    "page_size": paginator.page_size
                }
            }, status=status.HTTP_200_OK)
        
    
    def create(self, request):
        
        serializer = DeveloperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        developer = serializer.save()
        
        # Initialize skill levels for the new developer
        SkillLevelService.update_developer_skill_levels(developer)
        
        return Response({"details": "Developer created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        
        developer = Developers.objects.filter(id=pk).first()
        if not developer:
            return Response({"details": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        
        skills = DeveloperSkills.objects.filter(developer=developer)
        developer_projects = DeveloperProjects.objects.filter(developer=developer)
        # Group skills by skill area
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
        
        project_dict = []
        for project in developer_projects:
            project_dict.append({
                "project_id": project.id,
                "project_name": project.name,
                "project_description": project.description,
                "project_tech_stack": project.tech_stack,
                "project_origin": project.project_origin
            })
        
        # Convert to list format
        skills_grouped = list(skill_areas_dict.values())
        
        # Get skill levels with detailed information
        skill_levels_with_details = SkillLevelService.get_developer_skill_levels_with_details(developer)
        
        serializer = DeveloperSerializer(developer, context={'skills': skills_grouped})
        data = serializer.data
        data['skills'] = skill_levels_with_details  # Replace with skill levels instead of basic skills
        data['projects'] = project_dict
        return Response({"details": "Developer fetched successfully", "data": data}, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        
        developer = Developers.objects.filter(id=pk).first()
        if not developer:
            return Response({"details": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DeveloperSerializer(developer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({"details": "Developer updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        
        developer = Developers.object.filter(id=pk).first()
        if not developer:
            return Response({"details": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        
        developer.delete()
        
        return Response({"details": "Developer deleted successfully"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def add_dev_skills(self, request, pk=None):
        dev_id = request.data.get('dev_id')
        if dev_id:
            developer = Developers.objects.filter(id=dev_id).first()
            if not developer:
                return Response({"details": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
            skill_ids = request.data.get('skill_ids')
            if not skill_ids:
                return Response({"details": "Skill ids are required"}, status=status.HTTP_400_BAD_REQUEST)
            for skill_id in skill_ids:
                skill = Skills.objects.filter(id=skill_id).first()
                if not skill:
                    return Response({"details": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)
                skill_obj = DeveloperSkills.objects.filter(developer=developer, skill=skill).first()
                if skill_obj:
                    print("skill already exists: ", skill_obj)
                    #skill already exists
                    continue
                else:
                    #skill does not exist, create it
                    DeveloperSkills.objects.create(developer=developer, skill=skill)
            return Response({"details": "Skills added successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"details": "Developer id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def update_skill_levels(self, request):
        """Manually update skill levels for all developers or a specific developer."""
        dev_id = request.data.get('dev_id', None)
        
        if dev_id:
            # Update skill levels for a specific developer
            developer = Developers.objects.filter(id=dev_id).first()
            if not developer:
                return Response({"details": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
            
            SkillLevelService.update_developer_skill_levels(developer)
            return Response({"details": f"Skill levels updated for developer {developer.name}"}, status=status.HTTP_200_OK)
        else:
            # Update skill levels for all developers
            SkillLevelService.update_all_developers_skill_levels()
            return Response({"details": "Skill levels updated for all developers"}, status=status.HTTP_200_OK)
        
class SkillAreaViewSet(viewsets.ViewSet):
    
    def list(self, request):
        skill_areas = SkillAreas.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 12
        if skill_areas and skill_areas.count() > 0:
            paginated_skill_areas = paginator.paginate_queryset(skill_areas, request)
            serializer = SkillAreaSerializer(paginated_skill_areas, many=True)
            paginated_response = paginator.get_paginated_response(serializer.data)
            pagination_data = paginated_response.data
            count = pagination_data.get('count', 0)
            next_page = pagination_data.get('next', None)
            previous_page = pagination_data.get('previous', None)
            results = pagination_data.get('results', [])
            return Response({"details": "Skill areas fetched successfully", "data": results, "pagination": {
                "count": count,
                "next": next_page,
                "previous": previous_page,
                "current_page": request.GET.get('page', 1),
                "page_size": paginator.page_size
            }}, status=status.HTTP_200_OK)
        else:
            return Response({"details": "Skill areas fetched successfully", 
                             "data": [], 
                             "pagination": {
                "count": 0,
                "next": None,
                "previous": None,
                "current_page": 1,
                "page_size": paginator.page_size
            }}, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = SkillAreaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"details": "Skill area created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        skill_area = SkillAreas.objects.filter(id=pk).first()
        if not skill_area:
            return Response({"details": "Skill area not found"}, status=status.HTTP_404_NOT_FOUND)
        skills = Skills.objects.filter(skill_area=skill_area)
        skill_dict = []
        for skill in skills:
            skill_dict.append({
                "skill_id": skill.id,
                "skill_name": skill.name
            })
        return Response(
            {"details": "Skill area fetched successfully", 
             "data": {
                 "skill_area_id": skill_area.id,
                "skill_area": skill_area.name,
                "skills": skill_dict
             }}, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        return Response({"details": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, request, pk=None):
        return Response({"details": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @action(detail=False, methods=['post'])
    def add_skills(self, request):
        skill_area = request.data.get('skill_area', None)
        skill_ids = request.data.get('skill_id', None)
        skills = request.data.get('skills', None)
        if skill_area:
            # first save the skill area
            skill_area = SkillAreas.objects.create(name=skill_area)
            # then save the skill, skills will be a string separated by commas
            skills = skills.split(',')
            for skill in skills:
                Skills.objects.create(name=skill, skill_area=skill_area)
            return Response({"details": "Skills added successfully"}, status=status.HTTP_200_OK)
            
        elif skill_ids:
            skill_area = SkillAreas.objects.filter(id=skill_ids).first()
            if not skill_area:
                return Response({"details": "Skill area not found"}, status=status.HTTP_404_NOT_FOUND)
            skills = skills.split(',')
            for skill in skills:
                skill_obj = Skills.objects.filter(name=skill, skill_area=skill_area).first()
                if skill_obj:
                    #skill already exists
                    continue
                else:
                    #skill does not exist, create it
                    Skills.objects.create(name=skill, skill_area=skill_area)
            return Response({"details": "Skills added successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"details": "Skill area or skill id is required"}, status=status.HTTP_400_BAD_REQUEST)
                
class DeveloperProjectsViewSet(viewsets.ViewSet):
    
    def list(self, request):
        #apply filter by developer name
        developer_name = request.data.get('developer_name', None)
        if developer_name:
            developer_projects = DeveloperProjects.objects.filter(developer__name=developer_name)
        else:
            developer_projects = DeveloperProjects.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        if developer_projects and developer_projects.count() > 0:
            paginated_developer_projects = paginator.paginate_queryset(developer_projects, request)
            serializer = DeveloperProjectsListSerializer(paginated_developer_projects, many=True)
            paginated_response = paginator.get_paginated_response(serializer.data)
            pagination_data = paginated_response.data
            count = pagination_data.get('count', 0)
            next_page = pagination_data.get('next', None)
            previous_page = pagination_data.get('previous', None)
            results = pagination_data.get('results', [])
            return Response({"details": "Developer projects fetched successfully", "data": results, "pagination": {
                "count": count,
                "next": next_page,
                "previous": previous_page,
                "current_page": request.GET.get('page', 1),
                "page_size": paginator.page_size
            }}, status=status.HTTP_200_OK)
        else:
            return Response({"details": "Developer projects fetched successfully", "data": [], "pagination": {
                "count": 0,
                "next": None,
                "previous": None,
                "current_page": 1,
                "page_size": paginator.page_size
            }}, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = DeveloperProjectsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        
        # Update skill levels for the developer (this will also be triggered by signals)
        SkillLevelService.update_developer_skill_levels(project.developer)
        
        return Response({"details": "Developer project created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    
    
    def retrieve(self, request, pk=None):
        developer_project = DeveloperProjects.objects.filter(id=pk).first()
        if not developer_project:
            return Response({"details": "Developer project not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Get project categories with details
        project_categories = developer_project.project_categories.all()
        project_categories_data = []
        for category in project_categories:
            project_categories_data.append({
                "id": category.id,
                "name": category.name,
                "description": category.description
            })
        
        # Get skills grouped by skill area
        skills = developer_project.skills.all()
        skill_areas_dict = {}
        for skill in skills:
            skill_area_id = skill.skill_area.id
            skill_area_name = skill.skill_area.name
            
            if skill_area_id not in skill_areas_dict:
                skill_areas_dict[skill_area_id] = {
                    "skill_area_id": skill_area_id,
                    "skill_area_name": skill_area_name,
                    "skills": []
                }
            
            skill_areas_dict[skill_area_id]["skills"].append({
                "skill_id": skill.id,
                "skill_name": skill.name
            })
        
        skills_grouped = list(skill_areas_dict.values())
        
        serializer = DeveloperProjectsSerializer(developer_project)
        data = serializer.data
        data['project_categories'] = project_categories_data
        data['skills'] = skills_grouped
        
        return Response({"details": "Developer project fetched successfully", "data": data}, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        # can only update the description, tech_stack, project_origin, repo_link, doc_link, presentation_link, live_link
        developer_project = DeveloperProjects.objects.filter(id=pk).first()
        if not developer_project:
            return Response({"details": "Developer project not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
        serializer = DeveloperProjectsSerializer(developer_project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"details": "Developer project updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    
    