
# CareerBridge – Evidence-Based Interview Readiness

## Overview
CareerBridge is an AI-assisted interview readiness platform designed to help students prepare for placements using evidence-based resume analysis and interview feedback.

## Problem Statement
Students often include skills in resumes without sufficient project evidence and struggle to provide specific, structured interview answers. CareerBridge helps identify these gaps and supports transparent mentor review.

## Target Users
- Final-year placement students
- Placement-cell mentors

## Features
- Student profile and job description intake
- Resume upload and text extraction
- Resume skill analysis
- Claim vs Evidence checking
- Interview feedback interface
- Mentor review interface
- Student improvement planning

## Technology Stack
- Python
- Streamlit
- Nexus AI API
- PyPDF
- OpenAI-compatible Nexus SDK

## Responsible AI
- AI feedback should be treated as assistance, not a hiring decision.
- Students and mentors should verify all evidence.
- Unsupported claims must not be presented as verified facts.
- Human review is required for final decisions.
- Avoid uploading sensitive personal information unnecessarily.

## Installation

1. Clone the repository:
   git clone https://github.com/komalmakar513/CareerBridge.git

2. Open the project:
   cd CareerBridge

3. Create virtual environment:
   python -m venv venv

4. Activate it:
   Windows:
   venv\Scripts\activate

5. Install dependencies:
   pip install -r requirements.txt

6. Create a .env file:
   NEXUS_API_KEY=your_api_key
   NEXUS_BASE_URL=https://nexusapi.navigatelabs.ai
   NEXUS_MODEL=gpt-4o

7. Run the application:
   python -m streamlit run app.py

## AI Integration
CareerBridge is designed to use Nexus AI for AI-powered resume analysis and feedback. Valid Nexus credentials are required for these features.

## Project Status
UI and basic analysis modules have been developed. Nexus API validation and complete end-to-end team integration remain in progress.

## Repository
https://github.com/komalmakar513/CareerBridge