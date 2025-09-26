from google import genai
import logging
import os
import tempfile
from django.db.models import Q
from django.core.files.uploadedfile import UploadedFile
from developers.models import Developers, DeveloperSkills, DeveloperProjects, Skills, SkillAreas
from projects.models import ProjectCategory, ProjectCategorySkills

# File processing imports
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

logger = logging.getLogger(__name__)


class GeminiService:
    """
    Service class to handle Gemini API interactions
    """
    
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "gemini-2.5-flash"
    
    def extract_text_from_pdf(self, file) -> dict:
        """
        Extract text from PDF file
        
        Args:
            file: UploadedFile object
            
        Returns:
            dict: Success status and extracted text
        """
        if not PDF_AVAILABLE:
            return {
                "success": False,
                "error": "PyPDF2 library not installed. Please install it with: pip install PyPDF2",
                "text": ""
            }
        
        try:
            # Create a temporary file to save the uploaded content
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
            
            # Extract text from PDF
            with open(temp_file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            return {
                "success": True,
                "text": text.strip(),
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to extract text from PDF: {str(e)}",
                "text": ""
            }
    
    def extract_text_from_docx(self, file) -> dict:
        """
        Extract text from DOCX file
        
        Args:
            file: UploadedFile object
            
        Returns:
            dict: Success status and extracted text
        """
        if not DOCX_AVAILABLE:
            return {
                "success": False,
                "error": "python-docx library not installed. Please install it with: pip install python-docx",
                "text": ""
            }
        
        try:
            # Create a temporary file to save the uploaded content
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
            
            # Extract text from DOCX
            doc = Document(temp_file_path)
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            return {
                "success": True,
                "text": text.strip(),
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to extract text from DOCX: {str(e)}",
                "text": ""
            }
    
    def extract_text_from_file(self, file) -> dict:
        """
        Extract text from uploaded file based on file type
        
        Args:
            file: UploadedFile object
            
        Returns:
            dict: Success status and extracted text
        """
        if not file:
            return {
                "success": False,
                "error": "No file provided",
                "text": ""
            }
        
        # Get file extension
        file_extension = os.path.splitext(file.name)[1].lower()
        
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(file)
        elif file_extension == '.docx':
            return self.extract_text_from_docx(file)
        else:
            return {
                "success": False,
                "error": f"Unsupported file type: {file_extension}. Supported types: .pdf, .docx",
                "text": ""
            }
    
    def generate_content(self, query: str) -> dict:
        """
        Generate content using Gemini API
        
        Args:
            query (str): The query/prompt to send to Gemini
            
        Returns:
            dict: Response containing the generated content or error information
        """
        try:
            prompt = f"""
            You have to act like a Skilled and Professional Software Engineer with 10 years of experience in the following fields:
            - Python
            - Django
            - Machine Learning
            - Deep Learning
            - Computer Vision
            - Natural Language Processing
            - Web Development
            - AI Agent Development
            - AI Chatbot Development
            - AI Voice Assistant Development
            - AI Image Generation
            - AI Video Generation
            - AI Music Generation
            - AI Code Generation
            - Agentic Framework Development
            
            You have to give brief and concise answer to the user's query.
            User's query: {query}
            """
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            
            return {
                "success": True,
                "response": response.text,
                "model": self.model
            }
            
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "model": self.model
            }
    
    def get_developer_data(self, required_skills=None, project_categories=None):
        """
        Fetch developer data from database based on skills and project categories
        
        Args:
            required_skills (list): List of skill names
            project_categories (list): List of project category names
            
        Returns:
            dict: Developer data with their skills and projects
        """
        try:
            # Start with all available developers
            developers_query = Developers.objects.filter(is_available=True)
            
            # If specific skills are required, filter developers who have those skills
            if required_skills:
                skill_ids = Skills.objects.filter(name__in=required_skills).values_list('id', flat=True)
                developers_with_skills = DeveloperSkills.objects.filter(
                    skill_id__in=skill_ids
                ).values_list('developer_id', flat=True)
                developers_query = developers_query.filter(id__in=developers_with_skills)
            
            # Get developer data with their skills and projects
            developers_data = []
            for developer in developers_query:
                # Get developer skills
                developer_skills = DeveloperSkills.objects.filter(developer=developer).select_related('skill', 'skill__skill_area')
                skills_data = []
                for dev_skill in developer_skills:
                    skills_data.append({
                        'name': dev_skill.skill.name,
                        'skill_area': dev_skill.skill.skill_area.name
                    })
                
                # Get developer projects
                developer_projects = DeveloperProjects.objects.filter(developer=developer).prefetch_related('project_categories', 'skills')
                projects_data = []
                for project in developer_projects:
                    project_cats = [cat.name for cat in project.project_categories.all()]
                    project_skills = [skill.name for skill in project.skills.all()]
                    projects_data.append({
                        'name': project.name,
                        'description': project.description,
                        'tech_stack': project.tech_stack,
                        'project_origin': project.project_origin,
                        'project_categories': project_cats,
                        'skills_used': project_skills,
                        'repo_link': project.repo_link,
                        'live_link': project.live_link
                    })
                
                developers_data.append({
                    'id': developer.id,
                    'name': developer.name,
                    'email': developer.email,
                    'role': developer.role,
                    'industry_experience': developer.industry_experience,
                    'graduation_date': developer.graduation_date.isoformat(),
                    'employment_start_date': developer.employment_start_date.isoformat(),
                    'skills': skills_data,
                    'projects': projects_data
                })
            
            return {
                "success": True,
                "developers": developers_data,
                "total_count": len(developers_data)
            }
            
        except Exception as e:
            logger.error(f"Error fetching developer data: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "developers": []
            }
    
    def analyze_project_and_suggest_developers(self, project_name, project_description=None, project_file=None, required_skills=None, project_categories=None) -> dict:
        """
        Analyze project requirements and suggest suitable developers
        
        Args:
            project_name (str): Name of the project
            project_description (str): Optional description of the project (if not provided via file)
            project_file (UploadedFile): Optional file containing project description
            required_skills (list): Optional list of required skills
            project_categories (list): Optional list of project categories
            
        Returns:
            dict: Analysis and developer suggestions
        """
        try:
            # Handle project description - either from text or file
            final_project_description = project_description
            
            if project_file:
                # Extract text from uploaded file
                file_result = self.extract_text_from_file(project_file)
                if not file_result["success"]:
                    return {
                        "success": False,
                        "error": file_result["error"],
                        "model": self.model
                    }
                final_project_description = file_result["text"]
            
            # Validate that we have a project description
            if not final_project_description:
                return {
                    "success": False,
                    "error": "Project description is required. Provide either 'project_description' text or 'project_file'",
                    "model": self.model
                }
            
            # Get developer data from database
            developer_data_result = self.get_developer_data(required_skills, project_categories)
            
            if not developer_data_result["success"]:
                return developer_data_result
            
            developers = developer_data_result["developers"]
            
            if not developers:
                return {
                    "success": True,
                    "project_name": project_name,
                    "project_description": final_project_description,
                    "analysis": "No developers found matching the specified criteria.",
                    "suggested_developers": [],
                    "model": self.model
                }
            
            # Create prompt for Gemini analysis
            analysis_prompt = f"""
                You are an expert **Project Manager** and **Technical Salesperson**. 
                Analyze the given project requirements and available developers. 
                Your task is to recommend the most suitable developers ONLY using the information provided (no assumptions).

                ---

                ## PROJECT DETAILS
                - **Name:** {project_name}
                - **Description:** {final_project_description}
                - **Required Skills:** {required_skills or 'Not specified'}
                - **Project Categories:** {project_categories or 'Not specified'}

                ---

                ## AVAILABLE DEVELOPERS
                {self._format_developers_for_analysis(developers)}

                ---

                ## OUTPUT REQUIREMENTS
                You MUST respond in **clear Markdown** following the exact structure below.  
                Keep it **brief and to the point** (no more than 4–5 bullet points per section).  
                Do **not** invent or infer skills or experience not explicitly listed.  
                Do **not** repeat project details unnecessarily.  
                Use only developer data provided.

                ---

                ### RESPONSE STRUCTURE

                #### 1. Brief Analysis of Project
                - (2–3 bullet points summarizing key needs)

                #### 2. Required Skills & Technical Expertise
                - (List key skills & expertise required for the project, bullet format)

                #### 3. Top 3 Developer Recommendations
                For each developer, create a separate subsection. If less developers are available, then only display the approriate once:

                ##### Developer Rank. **Name**
                - **Score:** x/10  
                - **Why Suggested:** (1–3 concise bullet points)  
                - **Relevant Projects:** 
                    - **Project name**: description.
                    - **Link:** Links of project  
                - **Potential Concerns / Gaps:** (1–2 concise bullet points)

                ---

                ### ADDITIONAL INSTRUCTIONS
                - Use **Markdown headings**, lists and bold text exactly as shown.
                - Keep tone **neutral and professional**, avoid filler words.
                - Do NOT add APIs, libraries, or technologies not listed in developer data.
                - Always provide exactly 3 developer recommendations (ranked).
                """

            
            # Get Gemini's analysis
            gemini_response = self.generate_content(analysis_prompt)
            
            if not gemini_response["success"]:
                return gemini_response
            
            # Parse and structure the response
            return {
                "success": True,
                "project_name": project_name,
                "project_description": final_project_description,
                "required_skills": required_skills,
                "project_categories": project_categories,
                "total_developers_analyzed": len(developers),
                "analysis": gemini_response["response"],
                "model": self.model
            }
            
        except Exception as e:
            logger.error(f"Error analyzing project and suggesting developers: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "model": self.model
            }
    
    def _format_developers_for_analysis(self, developers):
        """
        Format developer data for Gemini analysis
        
        Args:
            developers (list): List of developer data
            
        Returns:
            str: Formatted string for analysis
        """
        formatted_data = ""
        for i, dev in enumerate(developers, 1):
            formatted_data += f"""
            DEVELOPER {i}:
            Name: {dev['name']}
            Role: {dev['role']}
            Industry Experience: {dev['industry_experience']} years
            Skills: {', '.join([skill['name'] for skill in dev['skills']])}
            Projects ({len(dev['projects'])} total):
            """
            
            for project in dev['projects'][:3]:  # Limit to first 3 projects for brevity
                formatted_data += f"""
                - {project['name']}: {project['description'][:100]}...
                  Tech Stack: {', '.join(project['tech_stack']) if project['tech_stack'] else 'Not specified'}
                  Categories: {', '.join(project['project_categories']) if project['project_categories'] else 'Not specified'}
                  Repo Link: {', '.join(project['repo_link']) if project['repo_link'] else 'Not Specified'} 
                """
            
            if len(dev['projects']) > 3:
                formatted_data += f"            ... and {len(dev['projects']) - 3} more projects\n"
            
            formatted_data += "\n"
        
        return formatted_data
