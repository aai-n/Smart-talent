# Smart Talent Selection Engine (HR Tech)

## 📌 Project Overview
The **Smart Talent Selection Engine** is a next-generation HR recruitment tool designed to solve the bottlenecks of traditional ATS (Applicant Tracking Systems). Instead of relying on rigid keyword matching, this engine uses semantic analysis to understand the intent and meaning behind a candidate's experience, ensuring high-potential talent isn't lost due to formatting or terminology differences.

## 🚀 Key Features

### 1. Multi-Format Resume Ingestion Portal
* **Robust Support:** Handles PDF, DocX, and high-quality image formats (JPG/PNG).
* **Intelligent Parsing:** Extracts text from non-linear layouts, two-column resumes, and tables without merging unrelated text blocks.
* **Real-time Feedback:** Provides upload progress and validation alerts for corrupt or unsupported files.
* **Batch Management:** Group resumes by "Job Role" or "Batch Date" for streamlined organization.

### 2. Semantic Profile & Intent Mapper
* **Skill Mapping:** Recognizes synonyms and hierarchies (e.g., understands that 'PyTorch' is a subset of 'Machine Learning').
* **Experience Extraction:** Automatically categorizes text into "Professional Experience," "Academic Projects," and "Certifications".
* **Profile Normalization:** Converts unstructured resume data into a standardized technical profile for easy comparison.

### 3. JD-to-Candidate Ranking Dashboard
* **Similarity Scoring:** Calculates a "Compatibility Score" (0-100%) based on how a candidate's profile aligns with a specific Job Description (JD).
* **Weighted Ranking:** Prioritizes depth of experience over simple mentions; for example, 5 years of experience ranks higher than a single project mention.
* **AI Justification:** Generates a 2-sentence "Summary of Fit" for top candidates to explain why they were ranked highly.

## 🛠️ Minimum End-to-End Expectations
1. **Recruiter Dashboard:** A central landing page showing active job roles, resume counts, and a "Top Talent" preview.
2. **Upload & Parsing View:** A clean interface for bulk-uploading with real-time extraction status.
3. **Ranking View:** A filterable table showing candidates ranked by score, years of experience, and the AI-generated justification snippet.

## 📂 Tech Stack (Suggested)
* **Frontend:** React.js / Next.js
* **Backend:** Python (FastAPI or Flask)
* **OCR & Parsing:** Tesseract OCR or AWS Textract for image-based resumes
* **NLP/AI:** OpenAI API (GPT-4) or Google Gemini API for semantic mapping and RAG-based ranking
* **Data Format:** Standardized JSON for normalized profiles

---
*Developed as a solution for the HR Tech: The "Smart Talent" Selection Engine requirements.*
