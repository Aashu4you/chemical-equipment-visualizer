import { Bar } from "react-chartjs-2";

function EquipmentTypeChart({ distribution }) {
  if (!distribution || Object.keys(distribution).length === 0) {
    return <p>No data available</p>;
  }

  const data = {
    labels: Object.keys(distribution),
    datasets: [
      {
        label: "Equipment Count",
        data: Object.values(distribution),
        backgroundColor: "#2d4a7c",
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
  };

  return (
    <div style={{ height: 350 }}>
      <Bar data={data} options={options} />
    </div>
  );
}

export default EquipmentTypeChart;
