from crewai import Task
from agents import doctor, verifier, nutritionist, exercise_specialist
from tools import BloodTestReportTool, NutritionTool, ExerciseTool

# Initialize tools
blood_test_tool = BloodTestReportTool()
nutrition_tool = NutritionTool()
exercise_tool = ExerciseTool()

# blood analysis Task
blood_analysis = Task(
    description=(
        "Analyze the blood test report at {file_path} and address any specific questions in {query}. "
        "Provide a professional interpretation of the results. Identify any "
        "abnormal values and their potential clinical significance. "
        "If there's a specific query, make sure to address it in your analysis."
    ),
    expected_output=(
        "A detailed blood test analysis report including:\n"
        "- Patient ID: [extracted from report]\n"
        "- Date of Test: [extracted date]\n"
        "- Summary of key findings\n"
        "- Abnormal values flagged with reference ranges\n"
        "- Potential clinical implications\n"
        "- Answers to any specific queries if provided\n"
        "- Recommended follow-up actions if needed"
    ),
    agent=doctor,
    tools=[blood_test_tool],
    output_file="output/blood_analysis.txt"
)

# Report verification task
report_verification = Task(
    description=(
        "Verify the blood test report at {file_path} and address any specific concerns in {query}. "
        "Check all values against standard ranges and "
        "flag any inconsistencies or missing information. "
        "If there's a specific query about the report's validity, address it directly."
    ),
    expected_output=(
        "A verification report containing:\n"
        "- Confirmation of report completeness\n"
        "- Validation of all measured values\n"
        "- Identification of any questionable results\n"
        "- Answers to any specific verification queries if provided\n"
        "- Recommendations for retesting if needed"
    ),
    agent=verifier,
    tools=[blood_test_tool],
    context=[blood_analysis],
    output_file="output/verification_report.txt"
)

# Nutrition analysis task
nutrition_analysis = Task(
    description=(
        "Create a personalized nutrition plan based on the blood test report at {file_path} "
        "and address any diet-related questions in {query}. Consider "
        "any abnormal values that may benefit from dietary changes. "
        "If there are specific nutrition questions, provide detailed answers."
    ),
    expected_output=("""**Nutrition Plan**
        - Key Findings: [Summary]
        - Dietary Recommendations:
        * [Specific food suggestions]
        * [Nutrients to increase]
        * [Nutrients to decrease]
        - Sample Meal Plan:
        * Breakfast: [Suggestion]
        * Lunch: [Suggestion]
        * Dinner: [Suggestion]
        - Answers to any specific nutrition queries if provided"""
    ),
    agent=nutritionist,
    tools=[nutrition_tool],
    output_file="output/nutrition.txt",
    context=[blood_analysis] 
)

# Exercise planning task
exercise_planning = Task(
    description=(
        "Create an exercise plan based on the blood test report at {file_path} "
        "and address any exercise-related questions in {query}. Consider "
        "any medical conditions or limitations indicated by the results. "
        "If there are specific exercise questions, provide detailed answers."
    ),
    expected_output=(
        """**Exercise Prescription**
        - Current Fitness Level: [Input level]
        - Recommended Activities:
        * [Activity 1]: [Duration/Frequency]
        * [Activity 2]: [Duration/Frequency]
        - Contraindications to note
        - Progression plan
        - Safety considerations
        - Answers to any specific exercise queries if provided"""
    ),
    agent=exercise_specialist,
    tools=[exercise_tool],
    context=[blood_analysis],    
    async_execution=False,
    output_file="output/exercise.txt"
)