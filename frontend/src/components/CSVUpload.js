import { useState } from "react";
import api from "../api";
import "./CSVUpload.css";

function CSVUpload({ onSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      // Validate file type
      if (!selectedFile.name.endsWith('.csv')) {
        alert("Please select a CSV file");
        return;
      }
      setFile(selectedFile);
    }
  };

  const upload = async () => {
    if (!file) {
      alert("Please select a CSV file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploading(true);
      await api.post("upload/", formData);
      alert("✅ Upload successful! Your data has been processed.");
      setFile(null); // Clear file after successful upload
      // Reset file input
      document.getElementById('csv-file-input').value = '';
      onSuccess();
    } catch (err) {
      console.error("Upload error:", err);
      alert("❌ Upload failed. Please check your file and try again.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="csv-upload-container">
      <div className="file-input-wrapper">
        <input
          type="file"
          id="csv-file-input"
          accept=".csv"
          onChange={handleFileChange}
        />
        <label 
          htmlFor="csv-file-input" 
          className={`file-input-label ${file ? 'has-file' : ''}`}
        >
          <span className="file-icon">
            {file ? '✅' : '📂'}
          </span>
          <div className="file-text">
            <div className="file-text-main">
              {file ? 'File Selected' : 'Choose CSV File'}
            </div>
            <div className="file-text-sub">
              {file ? 'Click to change file' : 'Click to browse or drag and drop'}
            </div>
          </div>
        </label>
        
        {file && (
          <div className="file-name">
            <span className="file-name-icon">📄</span>
            <span className="file-name-text">{file.name}</span>
            <span className="file-name-icon">
              {(file.size / 1024).toFixed(2)} KB
            </span>
          </div>
        )}
      </div>

      <div className="upload-actions">
        <button 
          className="upload-button" 
          onClick={upload}
          disabled={!file || uploading}
        >
          <span className="upload-button-icon">
            {uploading ? '⏳' : '⬆️'}
          </span>
          {uploading ? 'Uploading...' : 'Upload & Process'}
        </button>
      </div>
    </div>
  );
}

export default CSVUpload;