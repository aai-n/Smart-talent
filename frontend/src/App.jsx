import React, { useState } from 'react';

function App() {
  const [jobDescription, setJobDescription] = useState('');
  const [files, setFiles] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState([]);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!files || files.length === 0 || !jobDescription.trim()) {
      alert("Please provide both a Job Description and at least one resume.");
      return;
    }

    setIsAnalyzing(true);
    setResults([]);

    const formData = new FormData();
    formData.append('job_description', jobDescription);
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i]);
    }

    try {
      // Look for this line:
// const response = await fetch('http://localhost:8000/analyze', {

// CHANGE IT TO THIS:
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const response = await fetch(`${apiUrl}/analyze`, {
  method: 'POST',
  body: formData,
});
{
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error("Analysis failed:", error);
      alert("Failed to analyze candidates. Ensure the backend is running.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getScoreClass = (score) => {
    if (score >= 80) return 'score-high';
    if (score >= 60) return 'score-med';
    return 'score-low';
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1>Smart Talent Selection Engine</h1>
        <p>AI-Powered Semantic Resume Parsing & Ranking</p>
      </div>

      <div className="card">
        <form onSubmit={handleAnalyze}>
          <div className="form-group">
            <label>1. Paste Job Description</label>
            <textarea 
              placeholder="E.g. We are looking for a Senior Python Developer with experience in PyTorch and REST APIs..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label>2. Upload Candidate Resumes</label>
            <input 
              type="file" 
              multiple 
              accept=".pdf,.docx" 
              onChange={(e) => setFiles(e.target.files)}
              required 
            />
          </div>

          <button type="submit" className="btn-primary" disabled={isAnalyzing}>
            {isAnalyzing ? 'Analyzing Candidates with AI...' : 'Run Analysis'}
          </button>
        </form>
      </div>

      {results.length > 0 && (
        <div className="card">
          <h2 style={{ marginTop: 0, marginBottom: '20px' }}>Ranked Candidates</h2>
          <table className="results-table">
            <thead>
              <tr>
                <th>Match Score</th>
                <th>Candidate File</th>
                <th>Experience</th>
                <th>Top Matching Skills</th>
                <th>AI Justification</th>
              </tr>
            </thead>
            <tbody>
              {results.map(cand => (
                <tr key={cand.id}>
                  <td>
                    <span className={`score-badge ${getScoreClass(cand.compatibility_score)}`}>
                      {cand.compatibility_score}%
                    </span>
                  </td>
                  <td style={{ fontWeight: '500' }}>{cand.name}</td>
                  <td>{cand.years_experience}</td>
                  <td>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                      {cand.top_skills.map(skill => (
                        <span key={skill} className="skill-tag">{skill}</span>
                      ))}
                    </div>
                  </td>
                  <td style={{ fontSize: '0.9rem', color: '#475569', lineHeight: '1.4' }}>
                    {cand.ai_justification}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;