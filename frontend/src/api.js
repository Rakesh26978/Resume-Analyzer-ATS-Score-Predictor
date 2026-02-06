import axios from "axios";

export const analyzeResume = async (file, jd) => {
  const formData = new FormData();

  
  formData.append("resume", file);

 
  formData.append("job_description", jd);

  
  const response = await axios.post(
    "http://127.0.0.1:8000/analyze",
    formData
  );

  return response.data;
};
