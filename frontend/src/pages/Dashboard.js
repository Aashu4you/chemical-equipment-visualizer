import { useEffect, useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import CSVUpload from "../components/CSVUpload";
import UploadHistory from "../components/UploadHistory";
import EquipmentTable from "../components/EquipmentTable";
import EquipmentTypeChart from "../components/Charts/EquipmentTypeChart";
import AvgParametersChart from "../components/Charts/AvgParametersChart";
import "../components/Charts/chartSetup";
import "./App.css";

function Dashboard() {
  const navigate = useNavigate();
  const [equipment, setEquipment] = useState([]);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);

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
      // If unauthorized, redirect to login
      if (err.response && err.response.status === 401) {
        handleLogout();
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Get user data from localStorage
    const userData = localStorage.getItem("user");
    if (userData) {
      setUser(JSON.parse(userData));
    }

    loadData();

    const savedTheme = localStorage.getItem("darkMode");
    if (savedTheme === "true") setDarkMode(true);
  }, []);

  const toggleDarkMode = () => {
    setDarkMode((prev) => {
      localStorage.setItem("darkMode", !prev);
      return !prev;
    });
  };

  const handleLogout = () => {
    // Clear authentication data
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    
    // Navigate to login page
    navigate("/login");
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

    const csvContent = headers.join(",") + "\n" + rows.join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "filtered_equipment_data.csv";
    link.click();

    URL.revokeObjectURL(url);
  };

  const downloadPDF = () => {
    // Build URL with filter parameters
    const params = new URLSearchParams();
    
    if (selectedType !== "All") {
      params.append("type", selectedType);
    }
    
    if (searchText.trim()) {
      params.append("search", searchText.trim());
    }
    
    const url = `http://127.0.0.1:8000/api/generate-pdf/?${params.toString()}`;
    window.open(url, "_blank");
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
        <div className="header-left">
          <div className="brand-logo">
            <span className="logo-icon">⚗</span>
            <h1>ChemViz Dashboard</h1>
          </div>
        </div>
        
        <div className="header-right">
          {user && (
            <div className="user-info">
              <div className="user-avatar">
                {user.name ? user.name.charAt(0).toUpperCase() : "U"}
              </div>
              <span className="user-name">{user.name || user.email}</span>
            </div>
          )}
          
          <button className="theme-toggle" onClick={toggleDarkMode}>
            {darkMode ? "☀" : "🌙"}
          </button>
          
          <button className="logout-btn" onClick={handleLogout}>
            <span className="logout-icon">🚪</span>
            Logout
          </button>
        </div>
      </header>

      {/* Welcome Section */}
      <div className="welcome-section">
        <h2 className="welcome-title">
          Welcome back, {user?.name?.split(' ')[0] || 'User'}! 👋
        </h2>
        <p className="welcome-subtitle">
          Manage and visualize your chemical equipment data
        </p>
      </div>

      {/* CSV Upload */}
      <div className="section upload-section">
        <div className="section-header-with-icon">
          <div className="icon-title">
            <span className="section-icon">📁</span>
            <div>
              <h2>Data Management</h2>
              <p className="section-subtitle">
                Upload new equipment data or manage existing records
              </p>
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
              <p className="section-subtitle">
                Download filtered equipment data
              </p>
            </div>
          </div>
          <div className="data-count">
            {filteredEquipment.length}{" "}
            {filteredEquipment.length === 1 ? "record" : "records"}
          </div>
        </div>

        <div className="export-actions">
          <button
            className="export-btn"
            onClick={exportToCSV}
            disabled={filteredEquipment.length === 0}
          >
            <span className="btn-icon">📊</span>
            Export to CSV
          </button>

          <button
            className="export-btn pdf"
            onClick={downloadPDF}
            disabled={filteredEquipment.length === 0}
          >
            <span className="btn-icon">📄</span>
            Download PDF
          </button>
        </div>
      </div>

      {/* Equipment Table */}
      <div className="section">
        <h2>Equipment List</h2>
        {loading ? (
          <p>Loading equipment...</p>
        ) : (
          <EquipmentTable data={filteredEquipment} onDelete={loadData} />
        )}
      </div>

      {/* Upload History - Positioned AFTER Equipment Table */}
      <div className="section">
        <UploadHistory onRefresh={loadData} />
      </div>
    </div>
  );
}

export default Dashboard;