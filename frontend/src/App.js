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

  /* ===== FILTER LOGIC ===== */
  const equipmentTypes = useMemo(() => {
    return ["All", ...new Set(equipment.map((e) => e.equipment_type))];
  }, [equipment]);

  const filteredEquipment = useMemo(() => {
    if (selectedType === "All") return equipment;
    return equipment.filter((e) => e.equipment_type === selectedType);
  }, [equipment, selectedType]);

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

  return (
    <div className={`container ${darkMode ? "dark" : ""}`}>
      <header className="header">
        <h1>Chemical Equipment Dashboard</h1>
        <button className="theme-toggle" onClick={toggleDarkMode}>
          {darkMode ? "☀ Light Mode" : "🌙 Dark Mode"}
        </button>
      </header>

      {/* CSV Upload */}
      <div className="section">
        <h2>Upload CSV</h2>
        <CSVUpload onSuccess={loadData} />
      </div>

      {/* Filter */}
      <div className="section">
        <h2>Filter by Equipment Type</h2>
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
