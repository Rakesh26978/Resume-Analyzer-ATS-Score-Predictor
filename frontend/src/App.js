import React, { useState } from "react";
import { analyzeResume } from "./api";
import "./style.css";

export default function App() {
  const [step, setStep] = useState(1);

  const [file, setFile] = useState(null);
  const [jd, setJd] = useState("");
  const [result, setResult] = useState(null);

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    experience: "",
    skills: "",
    location: "",
  });

  const handleAnalyze = async () => {
    if (!file || !jd) {
      alert("Please upload resume and paste job description");
      return;
    }

    const data = await analyzeResume(file, jd);
    setResult(data);

    // Auto-fill fields
    setFormData({
      name: data.name,
      email: data.email,
      phone: data.phone,
      experience: "Fresher / Internship Experience",
      skills: "React, Node.js, MongoDB",
      location: "India",
    });

    setStep(2);
  };


  const handleApply = () => setStep(3);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };


  const handleSubmit = () => setStep(4);

  return (
    <div className="page">
      <div className="card">
        <h1 className="title">📄 RESUME ANALYZER & ATS SCORE PREDICTOR</h1>

        {/* STEP 1*/}
        {step === 1 && (
          <>
            <p className="subtitle">
              Upload your resume and predict ATS score instantly.
            </p>

            <div className="section">
              <label className="label">📄 Upload Resume (PDF)</label>
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => setFile(e.target.files[0])}
              />
            </div>

            <div className="section">
              <label className="label">📝 Job Description</label>
              <textarea
                rows="5"
                className="textarea"
                placeholder="Paste job description here..."
                value={jd}
                onChange={(e) => setJd(e.target.value)}
              />
            </div>

            <button className="primaryBtn" onClick={handleAnalyze}>
              🚀 Analyze Resume
            </button>
          </>
        )}

        {/*  STEP 2  */}
        {step === 2 && result && (
          <>
            <h2>📊 ATS Score Result</h2>

            <div className="scoreCard">
              <h1 style={{ color: "#2563eb" }}>{result.ats_score}%</h1>
              <p>Your resume match score for this job role</p>
            </div>

            <h3 style={{ marginTop: "20px" }}>
              Do you want to apply for this job?
            </h3>

            <button className="primaryBtn" onClick={handleApply}>
              ✅ Yes, Apply Now
            </button>

            <button className="secondaryBtn" onClick={() => setStep(1)}>
              ❌ No, Go Back
            </button>
          </>
        )}

        {/*  STEP 3 */}
        {step === 3 && (
          <>
            <h2>📋 Job Application Form</h2>

            <p className="subtitle">
              Some fields are auto-filled from your resume. You can edit them.
            </p>

            <div className="section">
              <label className="label">Full Name</label>
              <input
                className="input"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Enter your full name"
              />
            </div>

            <div className="section">
              <label className="label">Email Address</label>
              <input
                className="input"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Enter your email"
              />
            </div>

            <div className="section">
              <label className="label">Phone Number</label>
              <input
                className="input"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                placeholder="Enter phone number"
              />
            </div>

            <div className="section">
              <label className="label">Experience</label>
              <input
                className="input"
                name="experience"
                value={formData.experience}
                onChange={handleChange}
                placeholder="Fresher / 1 Year / Internship"
              />
            </div>

            <div className="section">
              <label className="label">Key Skills</label>
              <input
                className="input"
                name="skills"
                value={formData.skills}
                onChange={handleChange}
                placeholder="React, Node.js, MongoDB..."
              />
            </div>

            <div className="section">
              <label className="label">Current Location</label>
              <input
                className="input"
                name="location"
                value={formData.location}
                onChange={handleChange}
                placeholder="Enter your city"
              />
            </div>

            <button className="submitBtn" onClick={handleSubmit}>
              📩 Submit Application
            </button>
          </>
        )}

        {/*  STEP 4  */}
        {step === 4 && (
          <>
            <h2>🎉 Application Submitted!</h2>

            <div className="successBox">
              ✅ Thank you for applying. <br />
              📞 We will contact you shortly.
            </div>

            <button className="primaryBtn" onClick={() => setStep(1)}>
              🔄 Apply for Another Job
            </button>
          </>
        )}
      </div>
    </div>
  );
}
