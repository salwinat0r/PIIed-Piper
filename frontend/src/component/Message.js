import React, { useState } from 'react';
import axios from 'axios';
import './message.css'; // Import a CSS file to apply custom styles

const App = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState(null);

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
      });

      setDownloadUrl(`http://localhost:8000/${response.data.filename}`);
      setLoading(false);
    } catch (error) {
      console.error(error);
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (downloadUrl) {
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = 'output.pdf';
      link.click();
    }
  };

  return (
    <div>
      <h1>PDF Anonymizer</h1>
      <div>
        <input type="file" accept=".pdf" onChange={handleFileChange} />
        <button className="download-button" onClick={handleUpload} disabled={!selectedFile || loading}>
          Upload
        </button>
      </div>
      {loading && <div>Loading...</div>}
      {downloadUrl && (
        <div>
          <button className="download-button" onClick={handleDownload}>Download PDF</button>
        </div>
      )}
    </div>
  );
};

export default App;
