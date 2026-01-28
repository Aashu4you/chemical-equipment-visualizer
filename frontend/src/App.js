import { useEffect, useState } from "react";
import api from "./api";
import CSVUpload from "./components/CSVUpload";
import EquipmentTable from "./components/EquipmentTable";

function App() {
  const [equipment, setEquipment] = useState([]);
  const [summary, setSummary] = useState({});

  const loadData = async () => {
    const eq = await api.get("equipment/");
    const sum = await api.get("summary/");
    setEquipment(eq.data);
    setSummary(sum.data);
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Chemical Equipment Dashboard</h1>

      <CSVUpload onSuccess={loadData} />

      <h2>Summary</h2>
      <pre>{JSON.stringify(summary, null, 2)}</pre>

      <h2>Equipment List</h2>
      <EquipmentTable data={equipment} />
    </div>
  );
}

export default App;
