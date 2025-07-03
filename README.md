# 🧪 Blood Test Report Analyzer

An AI-powered system that analyzes blood test reports using professional medical agents such as a medical doctor, clinical nutritionist, and exercise specialist. Built with CrewAI and OpenAI.

---

##  Key Features

-  PDF blood test report ingestion and extraction
-  Multi-agent system with domain-specific expertise
-  Evidence-based and structured recommendations
-  Query-based response mechanism for health-related questions
-  FastAPI-based web interface

---

##  Fixed Issues

### 1. **Agents**
- Removed unprofessional/sarcastic behavior
- Added credentials and medical tone to agents
- Assigned tools properly per domain expertise
- Integrated query-response handling across agents

### 2. **Tools**
- Replaced `PDFLoader` with `pdfplumber` for accurate text extraction
- Added robust error handling for file issues
- Introduced Pydantic-based input schemas
- Added functions for key metric extraction from blood test reports

### 3. **Tasks**
- Implemented clear task division with role-specific responsibilities
- Improved context chaining between tasks
- Enabled structured response generation
- Each task now supports user queries effectively

### 4. **System Improvements**
- Centralized and safe LLM initialization with error handling
- Added type hints and docstrings for clarity
- Async/sync consistency across the FastAPI app
- Secure file upload and cleanup logic

---

## 📁 Project Structure

blood-test-analyzer/
├── agents.py # Professional medical agents
├── tasks.py # Well-defined analysis tasks
├── tools.py # Robust analysis tools
├── main.py # FastAPI application
├── requirements.txt # Python dependencies
└── README.md # Project documentation

## Setup Instructions

### 1. Clone the repository

- git clone https://github.com/your-username/blood-test-analyzer.git
- cd blood-test-analyzer

### 2. Create & Activate Virtual Environment (Optional but Recommended)

- python3 -m venv venv
- source venv/bin/activate

### 3. Install dependencies

- pip install -r requirements.txt

### 4. Set environment variables
Create a .env file in the root directory:

- OPENAI_API_KEY=your_openai_api_key

### 5. Running the API

- uvicorn main:app --reload



#  API Documentation — Blood Test Report Analyzer

This FastAPI-powered backend allows users to upload a blood test report PDF and receive a medically-informed analysis using AI agents.

---

##  `POST /analyze`

### Description
Uploads a PDF blood report and returns an AI-generated multi-agent medical analysis. You may also pass an optional query to receive focused answers.

---

### Request Parameters

| Parameter | Type   | Required | Description                          |
|-----------|--------|----------|--------------------------------------|
| file      | File   |  Yes     | Blood test report in PDF format       |
| query     | String |  No      | Optional question for the agents      |

---

### Example `curl` Request


curl -X POST http://localhost:8000/analyze \
  -F "file=@blood_test.pdf" \
  -F "query=What should I know about my cholesterol levels?"




## Key Technical Decisions

1. **PDF Processing**:
   - Chose `pdfplumber` over `PDFLoader` for better text extraction
   - Added comprehensive text cleaning

2. **Tool Design**:
   - BaseTool implementation for CrewAI compatibility
   - Separate metric extraction logic
   - Query-response integration

3. **Error Handling**:
   - Try-catch blocks in all tools
   - API exception handling
   - File operation safety

4. **LLM Integration**:
   - Centralized LLM configuration
   - Temperature control for medical accuracy
   - Retry mechanism

The system now provides reliable, professional blood test analysis with proper safety measures and documentation.