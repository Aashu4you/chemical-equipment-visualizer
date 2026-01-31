import { useEffect, useState } from "react";
import api from "../api";
import "./UploadHistory.css";

function UploadHistory({ onRefresh }) {
  const [batches, setBatches] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadBatches = async () => {
    try {
      setLoading(true);
      const res = await api.get("upload-batches/");
      setBatches(res.data);
    } catch (error) {
      console.error("Error loading batches:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    const confirmDelete = window.confirm(
      "⚠️ Are you sure you want to delete this upload and all its data?"
    );
    if (!confirmDelete) return;

    try {
      await api.delete(`upload-batch/${id}/`);
      alert("✅ Upload batch deleted successfully");
      await loadBatches();
      if (onRefresh) onRefresh();
    } catch (error) {
      console.error("Error deleting batch:", error);
      alert("❌ Failed to delete upload batch");
    }
  };

  useEffect(() => {
    loadBatches();
  }, []);

  return (
    <div className="upload-history-container">
      <div className="history-header">
        <div className="history-title-wrapper">
          <span className="history-icon">📜</span>
          <h2>Upload History</h2>
        </div>
        <span className="history-count">
          {batches.length} {batches.length === 1 ? "upload" : "uploads"}
        </span>
      </div>

      {loading ? (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading upload history...</p>
        </div>
      ) : batches.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📋</div>
          <h3>No Upload History</h3>
          <p>Upload a CSV file to see your upload history here.</p>
        </div>
      ) : (
        <table className="history-table">
          <thead>
            <tr>
              <th className="text-center">#</th>
              <th>File Name</th>
              <th>Uploaded At</th>
              <th className="text-right">Records</th>
              <th className="text-right">Avg Flowrate</th>
              <th className="text-right">Avg Pressure</th>
              <th className="text-right">Avg Temp</th>
              <th className="text-center">Action</th>
            </tr>
          </thead>
          <tbody>
            {batches.map((batch, index) => (
              <tr key={batch.id}>
                <td className="text-center index-cell">{index + 1}</td>
                <td className="filename-cell">
                  <span className="file-icon">📄</span>
                  {batch.filename}
                </td>
                <td className="date-cell">
                  {new Date(batch.uploaded_at).toLocaleString()}
                </td>
                <td className="text-right numeric-cell">{batch.total_records}</td>
                <td className="text-right numeric-cell">
                  {batch.avg_flowrate.toFixed(2)}
                </td>
                <td className="text-right numeric-cell">
                  {batch.avg_pressure.toFixed(2)}
                </td>
                <td className="text-right numeric-cell">
                  {batch.avg_temperature.toFixed(2)}
                </td>
                <td className="text-center">
                  <button
                    className="history-delete-btn"
                    onClick={() => handleDelete(batch.id)}
                    title="Delete upload batch"
                  >
                    <span className="delete-icon">🗑️</span>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default UploadHistory;