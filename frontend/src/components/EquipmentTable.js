import React from "react";
import api from "../api";
import "./EquipmentTable.css";

function EquipmentTable({ data, onDelete }) {
  const handleDelete = async (id) => {
    const confirmDelete = window.confirm(
      "⚠️ Are you sure you want to delete this equipment?"
    );

    if (!confirmDelete) return;

    try {
      await api.delete(`equipment/${id}/`);
      alert("✅ Equipment deleted successfully");
      onDelete(); // Reload data
    } catch (error) {
      console.error("Error deleting equipment:", error);
      alert("❌ Failed to delete equipment");
    }
  };
  const handleDeleteAll = async () => {
  const confirmDelete = window.confirm(
    "⚠️ This will delete ALL equipment data.\n\nThis action cannot be undone. Continue?"
  );

  if (!confirmDelete) return;

  try {
    await api.delete("equipment/delete-all/");
    alert("✅ All equipment data deleted successfully");
    onDelete(); // Reload data
  } catch (error) {
    console.error("Error deleting all equipment:", error);
    alert("❌ Failed to delete all equipment data");
  }
};


  if (!data || data.length === 0) {
    return (
      <div className="table-empty">
        <p>No equipment data available</p>
      </div>
    );
  }

  return (
  <>
    <table className="equipment-table">
      <thead>
        <tr>
          <th className="text-center">Sr. No</th>
          <th>Equipment Name</th>
          <th>Type</th>
          <th className="text-right">Flowrate</th>
          <th className="text-right">Pressure</th>
          <th className="text-right">Temperature</th>
          <th className="text-center">Actions</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item, index) => (
          <tr key={item.id}>
            <td className="text-center id-cell">{index + 1}</td>
            <td className="equipment-name">{item.equipment_name}</td>
            <td>
              <span className="type-badge">{item.equipment_type}</span>
            </td>
            <td className="text-right numeric-cell">
              {Number(item.flowrate).toFixed(2)}
            </td>
            <td className="text-right numeric-cell">
              {Number(item.pressure).toFixed(2)}
            </td>
            <td className="text-right numeric-cell">
              {Number(item.temperature).toFixed(2)}
            </td>
            <td className="text-center">
              <button
                className="delete-btn"
                onClick={() => handleDelete(item.id)}
                title="Delete equipment"
              >
                <span className="delete-icon">🗑️</span>
                Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>

    {/* 🔥 DELETE ALL BUTTON */}
    <div className="delete-all-container">
      <button
        className="delete-all-btn"
        onClick={handleDeleteAll}
      >
        ❌ Delete All Data
      </button>
    </div>
  </>
);

}

export default EquipmentTable;
