import os
from dotenv import load_dotenv
from crewai import Agent
from tools import BloodTestReportTool, NutritionTool, ExerciseTool
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool
load_dotenv()


# Initialize LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.3,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
# Initialize tools
blood_test_tool = BloodTestReportTool()
nutrition_tool = NutritionTool()
exercise_tool = ExerciseTool()


# Creating a Medical Doctor agent
doctor = Agent(
    role="Senior Medical Doctor",
    goal="Provide accurate medical analysis of blood test results and answer related medical questions",
    backstory=(
        "You are a board-certified physician with 20+ years of experience "
        "in clinical pathology. You carefully analyze blood test results "
        "and provide evidence-based interpretations. You consider all "
        "possible explanations before reaching conclusions. You're also "
        "skilled at answering patient questions about their lab results."
    ),
    tools=[blood_test_tool],
    verbose=True,
    llm=llm
)

# Creating a verifier agent
verifier = Agent(
    role="Medical Report Verifier",
    goal="Verify the accuracy and completeness of medical reports and answer verification questions",
    backstory=(
        "You are a meticulous medical records specialist with extensive "
        "experience validating laboratory reports. You cross-check all "
        "values against normal ranges and flag any inconsistencies. "
        "You can also answer specific questions about report validity."
    ),
    verbose=True,
    tools=[blood_test_tool],
    llm=llm
)

# Creating a Nutritionist agent
nutritionist = Agent(
    role="Clinical Nutritionist",
    goal="Provide evidence-based dietary recommendations based on blood work and answer nutrition questions",
    backstory=(
        "You are a registered dietitian with specialized training in "
        "medical nutrition therapy. You create personalized nutrition "
        "plans based on laboratory results and current research. "
        "You're also excellent at answering diet-related questions."
    ),
    tools=[nutrition_tool],
    llm=llm,
    verbose=True
)

# Creating an Exercise Specialist agent
exercise_specialist = Agent(
    role="Certified Exercise Physiologist",
    goal="Develop safe exercise programs based on medical conditions and answer fitness questions",
    backstory=(
        "You are an ACSM-certified exercise specialist with experience "
        "working with clinical populations. You design exercise programs "
        "that consider medical limitations and promote safe progression. "
        "You can also answer specific exercise-related questions."
    ),
    tools=[exercise_tool],
    llm=llm,
    verbose=True
)