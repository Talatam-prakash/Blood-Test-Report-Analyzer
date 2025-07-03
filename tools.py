## Importing libraries and files
import os
from dotenv import load_dotenv
import pdfplumber  
import re
from typing import Type, List, ClassVar, Dict, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI

load_dotenv()


# Initialize LLM with error handling
try:
    llm: ChatOpenAI = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.3,
        api_key=os.getenv("OPENAI_API_KEY", "")
    )
except Exception as e:
    raise RuntimeError(f"Failed to initialize LLM: {str(e)}")


#----------------------- Blood Test Report Tool -----------------------#
class BloodTestInput(BaseModel):
    """Input schema for blood test analysis tools."""
    path: str = Field(..., description="Path to the PDF blood test report")
    query: Optional[str] = Field(None, description="Optional question about the blood test results")

class BloodTestReportTool(BaseTool):
    """Tool to read and extract data from blood test PDF reports and answer questions."""
    name: str = "blood_test_reader"
    description: str = "Extracts and cleans data from blood test PDF reports and answers questions about the results"
    args_schema: Type[BaseModel] = BloodTestInput
    llm: ClassVar[ChatOpenAI] = llm
 
    def _run(self, path: str, query: Optional[str] = None) -> str:
        """
        Load and process blood test report from PDF and optionally answer a query.
        
        Args:
            path (str): Path to the PDF file
            query (str, optional): Question about the blood test results
            
        Returns:
            str: Cleaned and formatted blood test report with query response if provided
        """
        try:
            full_report = ""
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text = re.sub(r'\s+', ' ', text).strip()
                        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
                        full_report += text + "\n\n"
            
            if not full_report.strip():
                raise ValueError("PDF contained no extractable text")
            
            if query:
                response = self.llm.invoke(
                    f"Blood Test Report:\n{full_report}\n\nQuestion: {query}\n\nAnswer:"
                )
                return f"REPORT:\n{full_report}\n\nQUERY RESPONSE:\n{response.content}"
                
            return full_report
            
        except Exception as e:
            return f"Error processing PDF: {str(e)}"
    
#----------------------- Nutrition Tool -----------------------#
class NutritionInput(BaseModel):
    """Input schema for nutrition analysis."""
    blood_report: str = Field(..., description="The blood test report text")
    query: Optional[str] = Field(None, description="Optional nutrition-related question")
    focus_areas: Optional[list] = Field(None, description="Specific health markers to focus on")

class NutritionTool(BaseTool):
    """Analyzes blood test results and provides dietary recommendations and answers questions."""
    name: str = "nutrition_analyzer"
    description: str = "Provides dietary recommendations based on blood test results and answers nutrition questions"
    args_schema: Type[BaseModel] = NutritionInput
    llm: ClassVar[ChatOpenAI] = llm
 
    def _run(self, blood_report: str, query: Optional[str] = None, focus_areas: Optional[list] = None) -> str:
        """
        Analyze blood report and generate nutrition recommendations and answer questions.
        """
        try:
            metrics = self._extract_metrics(blood_report)
            recommendations = []
            
            if metrics.get('glucose', 0) > 100:
                recommendations.append("- Reduce sugar and refined carb intake")
            if metrics.get('hdl', 0) < 40:
                recommendations.append("- Increase healthy fats (avocados, nuts, olive oil)")
            if not recommendations:
                recommendations.append("- Maintain balanced diet with variety of whole foods")
            
            base_response = "\n".join([
                "Nutrition Recommendations:",
                *recommendations,
                "\nBased on analysis of your blood test results"
            ])
            
            if query:
                q_response = self.llm.invoke(
                    f"Blood Test Metrics:\n{metrics}\n\nQuestion: {query}\n\nAnswer:"
                )
                return f"{base_response}\n\nQUESTION ANSWER:\n{q_response.content}"
                
            return base_response
            
        except Exception as e:
            return f"Error generating nutrition recommendations: {str(e)}"
    def _extract_metrics(self, report_text: str) -> dict:
        """Helper to extract numeric values from report text."""
        metrics = {}
        patterns = {
            'glucose': r'Glucose\s*(\d+)',
            'hdl': r'HDL\s*(\d+)',
            'ldl': r'LDL\s*(\d+)'
        }
        
        for name, pattern in patterns.items():
            match = re.search(pattern, report_text, re.IGNORECASE)
            if match:
                metrics[name] = float(match.group(1))
                
        return metrics

#----------------------- Exercise Tool -----------------------#
class ExerciseInput(BaseModel):
    """Input schema for exercise planning."""
    blood_report: str = Field(..., description="The blood test report text")
    query: Optional[str] = Field(None, description="Optional exercise-related question")
    activity_level: Optional[str] = Field("moderate", description="Current activity level")

class ExerciseTool(BaseTool):
    """Creates personalized exercise plans based on blood test results and answers questions."""
    name: str = "exercise_planner"
    description: str = "Generates exercise recommendations based on blood work and answers fitness questions"
    args_schema: Type[BaseModel] = ExerciseInput
    llm: ClassVar[ChatOpenAI] = llm
 
    def _run(self, blood_report: str, query: Optional[str] = None, activity_level: str = "moderate") -> str:
        """
        Generate exercise recommendations based on blood test results and answer questions.
        """
        try:
            metrics = self._extract_metrics(blood_report)
            recommendations = []
            
            if activity_level == "low":
                recommendations.append("- Start with 20-30 min walks daily")
            else:
                recommendations.append("- 30-45 min cardio 4-5x/week")
            if metrics.get('hemoglobin', 0) < 12:
                recommendations.append("- Include iron-boosting activities like swimming")
            
            base_response = "\n".join([
                "Exercise Recommendations:",
                *recommendations,
                "\nAdjust intensity based on how you feel"
            ])
            
            if query:
                q_response = self.llm.invoke(
                    f"Blood Test Metrics:\n{metrics}\n\nQuestion: {query}\n\nAnswer:"
                )
                return f"{base_response}\n\nQUESTION ANSWER:\n{q_response.content}"
                
            return base_response
            
        except Exception as e:
            return f"Error generating exercise plan: {str(e)}"
    def _extract_metrics(self, report_text: str) -> dict:
        """Helper to extract numeric values from report text."""
        metrics = {}
        patterns = {
            'hemoglobin': r'Hemoglobin\s*([\d.]+)',
            'hematocrit': r'Hematocrit\s*([\d.]+)'
        }
        
        for name, pattern in patterns.items():
            match = re.search(pattern, report_text, re.IGNORECASE)
            if match:
                metrics[name] = float(match.group(1))
                
        return metrics
# Initialize tools
search_tool = SerperDevTool()
blood_test_tool = BloodTestReportTool()
nutrition_tool = NutritionTool()
exercise_tool = ExerciseTool()