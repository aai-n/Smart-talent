import io
import json
import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from google import genai
import PyPDF2
import docx
from dotenv import load_dotenv

# Load the hidden environment variables from the .env file
load_dotenv()

app = FastAPI(title="AIzaSyBnRwezJwSGPkzPRNYDdeJuV1QXsYjsgAI")

# Enable CORS so the React frontend can communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIGURE GEMINI SECURELY ---
# This pulls the key from your hidden .env file
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini client
client = genai.Client(api_key=api_key)

def extract_text(file_bytes, filename):
    """Extracts text from PDF or DocX bytes."""
    filename = filename.lower()
    if filename.endswith('.pdf'):
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        except Exception as e: 
            print(f"PDF extraction error: {e}")
            return ""
    elif filename.endswith('.docx'):
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            return " ".join([para.text for para in doc.paragraphs])
        except Exception as e:
            print(f"DocX extraction error: {e}")
            return ""
    return ""

@app.post("/analyze")
async def analyze_candidates(job_description: str = Form(...), files: List[UploadFile] = File(...)):
    results = []

    for file in files:
        # Read the file contents into memory
        file_bytes = await file.read()
        resume_text = extract_text(file_bytes, file.filename)
        
        if not resume_text.strip():
            print(f"Warning: Could not extract text from {file.filename}")
            continue

        # AI Prompt
        prompt = f"""
        Analyze the following Resume against the Job Description (JD).
        
        JD: {job_description}
        
        Resume: {resume_text}
        
        Provide the output strictly in valid JSON format with these exact keys:
        - "compatibility_score": A number between 0 and 100.
        - "years_experience": A short string summarizing extracted years of relevant experience.
        - "top_skills": An array of strings representing the top matching skills.
        - "ai_justification": A 2-sentence summary explaining exactly why they were ranked this way based on the JD.
        """
        
        try:
            # Send the prompt to the new Gemini model
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            # Clean up JSON formatting to ensure it parses correctly
            response_text = response.text.replace('```json', '').replace('```', '').strip()
            result_json = json.loads(response_text)
            
            # Add the structured data to our results list
            results.append({
                "id": str(len(results) + 1),
                "name": file.filename.rsplit('.', 1)[0], # Use filename without extension as name
                "years_experience": result_json.get("years_experience", "N/A"),
                "top_skills": result_json.get("top_skills", []),
                "compatibility_score": result_json.get("compatibility_score", 0),
                "ai_justification": result_json.get("ai_justification", "")
            })
        except Exception as e:
            print(f"Error analyzing {file.filename}: {e}")
            continue

    # Sort results by highest compatibility score first
    results.sort(key=lambda x: x["compatibility_score"], reverse=True)
    return results