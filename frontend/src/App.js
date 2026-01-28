import { useEffect, useState } from "react";
import api from "./api";
import CSVUpload from "./components/CSVUpload";
import EquipmentTable from "./components/EquipmentTable";
import EquipmentTypeChart from "./components/Charts/EquipmentTypeChart";
import AvgParametersChart from "./components/Charts/AvgParametersChart";
import "./components/Charts/chartSetup";
import "./App.css";

function App() {
  const [equipment, setEquipment] = useState([]);
  const [summary, setSummary] = useState({});
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const eq = await api.get("equipment/");
      const sum = await api.get("summary/");
      setEquipment(eq.data);
      setSummary(sum.data);
    } catch (err) {
      console.error("Error loading data", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const formatNumber = (num) => {
    if (num === null || num === undefined) return "N/A";
    return typeof num === "number" ? num.toFixed(2) : num;
  };

  return (
    <div className="container">
      <h1>Chemical Equipment Dashboard</h1>

      <div className="section">
        <h2>Upload CSV</h2>
        <CSVUpload onSuccess={loadData} />
      </div>

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

      <div className="section">
        <h2>Equipment Type Distribution</h2>
        {!loading && (
          <EquipmentTypeChart
            distribution={summary.equipment_type_distribution}
          />
        )}
      </div>

      <div className="section">
        <h2>Average Operating Parameters</h2>
        {!loading && <AvgParametersChart summary={summary} />}
      </div>

      <div className="section">
        <h2>Equipment List</h2>
        {loading ? <p>Loading equipment...</p> : <EquipmentTable data={equipment} />}
      </div>
    </div>
  );
}

export default App;