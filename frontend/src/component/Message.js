import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [outputFile, setOutputFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      setLoading(true);

      const response = await axios.post('http://localhost:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        responseType: 'blob',
      });

      const outputPdf = new Blob([response.data], { type: 'application/pdf' });
      setOutputFile(URL.createObjectURL(outputPdf));
      setLoading(false);
    } catch (error) {
      console.error(error);
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>PDF Anonymizer</h1>
      <div>
        <input type="file" accept=".pdf" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={!selectedFile || loading}>
          Upload
        </button>
      </div>
      {loading && <div>Loading...</div>}
      {outputFile && (
        <div>
          <h2>Output PDF</h2>
          <iframe src={outputFile} width="100%" height="600px" title="Output PDF" />
        </div>
      )}
    </div>
  );
};

export default App;
