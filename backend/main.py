import io
import json
import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from google import genai
import PyPDF2
import docx
from dotenv import load_dotenv # Import this to read .env files

# --- 1. LOAD THE SECRETS ---
load_dotenv() # This looks for a file named .env in your folder
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # This will show up in your Render Logs if you forgot to add the key there!
    print("CRITICAL ERROR: GEMINI_API_KEY is missing from the environment!")
else:
    print("Success: API Key loaded successfully.")

app = FastAPI(title="Smart Talent Backend")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. INITIALIZE THE CLIENT SECURELY ---
if not api_key:
    print("WARNING: GEMINI_API_KEY not found in environment variables!")
client = genai.Client(api_key=api_key)

def extract_text(file_bytes, filename):
    filename = filename.lower()
    if filename.endswith('.pdf'):
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
            return text
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
    
    print(f"--- New Request ---")
    print(f"Files received: {[f.filename for f in files]}")

    for file in files:
        file_bytes = await file.read()
        resume_text = extract_text(file_bytes, file.filename)
        
        if not resume_text.strip():
            print(f"Skipping {file.filename}: No text extracted.")
            continue

        prompt = f"""
        Analyze the following Resume against the Job Description (JD).
        JD: {job_description}
        Resume: {resume_text}
        Provide the output strictly in valid JSON format with these exact keys:
        - "compatibility_score": A number between 0 and 100.
        - "years_experience": A short string.
        - "top_skills": An array of strings.
        - "ai_justification": A 2-sentence summary.
        """
        
        try:
            # Use 'gemini-2.0-flash' for best results
            response = client.models.generate_content(
                model='gemini-2.0-flash', 
                contents=prompt,
            )
            
            # Clean and parse JSON
            response_text = response.text.replace('```json', '').replace('```', '').strip()
            result_json = json.loads(response_text)
            
            results.append({
                "id": str(len(results) + 1),
                "name": file.filename.rsplit('.', 1)[0],
                "years_experience": result_json.get("years_experience", "N/A"),
                "top_skills": result_json.get("top_skills", []),
                "compatibility_score": result_json.get("compatibility_score", 0),
                "ai_justification": result_json.get("ai_justification", "")
            })
            print(f"Successfully analyzed: {file.filename}")

        except Exception as e:
            print(f"Error analyzing {file.filename}: {e}")
            continue

    results.sort(key=lambda x: x["compatibility_score"], reverse=True)
    print(f"Returning {len(results)} results.")
    return results