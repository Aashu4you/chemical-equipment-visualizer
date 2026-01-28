import { useState } from "react";
import api from "../api";

function CSVUpload({ onSuccess }) {
  const [file, setFile] = useState(null);

  const upload = async () => {
    if (!file) return alert("Select a CSV file");

    const formData = new FormData();
    formData.append("file", file);

    try {
      await api.post("upload/", formData);
      alert("Upload successful");
      onSuccess();
    } catch (err) {
      alert("Upload failed");
    }
  };

  return (
    <div>
      <h3>Upload CSV</h3>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={upload}>Upload</button>
    </div>
  );
}

export default CSVUpload;
