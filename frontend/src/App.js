import { useEffect, useState, useMemo } from "react";
import api from "./api";
import CSVUpload from "./components/CSVUpload";
import EquipmentTable from "./components/EquipmentTable";
import EquipmentTypeChart from "./components/Charts/EquipmentTypeChart";
import AvgParametersChart from "./components/Charts/AvgParametersChart";
import "./components/Charts/chartSetup";
import "./App.css";

function App() {
  const [equipment, setEquipment] = useState([]);
  const [loading, setLoading] = useState(true);

  // filter
  const [selectedType, setSelectedType] = useState("All");

  // search
  const [searchText, setSearchText] = useState("");

  // dark mode
  const [darkMode, setDarkMode] = useState(false);

  const loadData = async () => {
    try {
      setLoading(true);
      const eq = await api.get("equipment/");
      setEquipment(eq.data);
    } catch (err) {
      console.error("Error loading data", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();

    // load saved theme
    const savedTheme = localStorage.getItem("darkMode");
    if (savedTheme === "true") setDarkMode(true);
  }, []);

  const toggleDarkMode = () => {
    setDarkMode((prev) => {
      localStorage.setItem("darkMode", !prev);
      return !prev;
    });
  };

  /* ===== FILTER OPTIONS ===== */
  const equipmentTypes = useMemo(() => {
    return ["All", ...new Set(equipment.map((e) => e.equipment_type))];
  }, [equipment]);

  /* ===== FILTER + SEARCH LOGIC ===== */
  const filteredEquipment = useMemo(() => {
    return equipment.filter((e) => {
      const matchesType =
        selectedType === "All" || e.equipment_type === selectedType;

      const matchesSearch =
        e.equipment_name
          ?.toLowerCase()
          .includes(searchText.toLowerCase());

      return matchesType && matchesSearch;
    });
  }, [equipment, selectedType, searchText]);

  /* ===== SUMMARY FROM FILTERED DATA ===== */
  const summary = useMemo(() => {
    if (filteredEquipment.length === 0) {
      return {
        total_equipment: 0,
        avg_flowrate: 0,
        avg_pressure: 0,
        avg_temperature: 0,
        equipment_type_distribution: {},
      };
    }

    const total = filteredEquipment.length;

    const avg = (key) =>
      filteredEquipment.reduce((sum, e) => sum + Number(e[key]), 0) / total;

    const distribution = {};
    filteredEquipment.forEach((e) => {
      distribution[e.equipment_type] =
        (distribution[e.equipment_type] || 0) + 1;
    });

    return {
      total_equipment: total,
      avg_flowrate: avg("flowrate"),
      avg_pressure: avg("pressure"),
      avg_temperature: avg("temperature"),
      equipment_type_distribution: distribution,
    };
  }, [filteredEquipment]);

  const formatNumber = (num) => {
    if (num === null || num === undefined || isNaN(num)) return "N/A";
    return Number(num).toFixed(2);
  };

  const exportToCSV = () => {
    if (filteredEquipment.length === 0) {
      alert("No data to export");
      return;
    }

    const headers = Object.keys(filteredEquipment[0]);

    const rows = filteredEquipment.map((item) =>
      headers.map((h) => `"${item[h]}"`).join(",")
    );

    const csvContent =
      headers.join(",") + "\n" + rows.join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "filtered_equipment_data.csv";
    link.click();

    URL.revokeObjectURL(url);
  };

  const clearAllData = async () => {
    const confirmClear = window.confirm(
      "⚠ This will delete ALL equipment data. Are you sure?"
    );

    if (!confirmClear) return;

    try {
      await api.delete("equipment/clear/");
      await loadData();
      alert("✅ All equipment data cleared successfully");
    } catch (error) {
      console.error("Error clearing data", error);
      alert("❌ Failed to clear data");
    }
  };

  return (
    <div className={`container ${darkMode ? "dark" : ""}`}>
      <header className="header">
        <h1>Chemical Equipment Dashboard</h1>
        <button className="theme-toggle" onClick={toggleDarkMode}>
          {darkMode ? "☀ Light Mode" : "🌙 Dark Mode"}
        </button>
      </header>

      {/* CSV Upload */}
      <div className="section upload-section">
        <div className="section-header-with-icon">
          <div className="icon-title">
            <span className="section-icon">📁</span>
            <div>
              <h2>Data Management</h2>
              <p className="section-subtitle">Upload new equipment data or manage existing records</p>
            </div>
          </div>
        </div>
        <div className="upload-content">
          <CSVUpload onSuccess={loadData} />
        </div>
      </div>

      {/* Filter + Search */}
      <div className="section filter-search-row">
        <div className="filter-box">
          <label>Filter by Equipment Type</label>
          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
          >
            {equipmentTypes.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-box">
          <label>Search Equipment</label>
          <input
            type="text"
            placeholder="Search by equipment name..."
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
          />
        </div>
      </div>

      {/* Summary */}
      <div className="section">
        <h2>Summary</h2>
        {loading ? (
          <p>Loading summary...</p>
        ) : (
          <div className="cards">
            <div className="card">
              Total Equipment
              <span>{summary.total_equipment}</span>
            </div>
            <div className="card">
              Avg Flowrate
              <span>{formatNumber(summary.avg_flowrate)}</span>
            </div>
            <div className="card">
              Avg Pressure
              <span>{formatNumber(summary.avg_pressure)}</span>
            </div>
            <div className="card">
              Avg Temperature
              <span>{formatNumber(summary.avg_temperature)}</span>
            </div>
          </div>
        )}
      </div>

      {/* Charts */}
      <div className="charts-row">
        <div className="section chart-box">
          <h2>Equipment Type Distribution</h2>
          {!loading && (
            <EquipmentTypeChart
              distribution={summary.equipment_type_distribution}
            />
          )}
        </div>

        <div className="section chart-box">
          <h2>Average Operating Parameters</h2>
          {!loading && <AvgParametersChart summary={summary} />}
        </div>
      </div>

      {/* Export Section */}
      <div className="section export-section">
        <div className="section-header-with-icon">
          <div className="icon-title">
            <span className="section-icon">⬇️</span>
            <div>
              <h2>Export Data</h2>
              <p className="section-subtitle">Download filtered equipment data as CSV</p>
            </div>
          </div>
          <div className="data-count">
            {filteredEquipment.length} {filteredEquipment.length === 1 ? 'record' : 'records'}
          </div>
        </div>
        <button 
          className="export-btn" 
          onClick={exportToCSV}
          disabled={filteredEquipment.length === 0}
        >
          <span className="btn-icon">📊</span>
          Export to CSV
        </button>
      </div>

      {/* Table */}
      <div className="section">
        <h2>Equipment List</h2>
        {loading ? (
          <p>Loading equipment...</p>
        ) : (
          <EquipmentTable data={filteredEquipment} />
        )}
      </div>
    </div>
  );
}

export default App;