import { Bar } from "react-chartjs-2";

function AvgParametersChart({ summary }) {
  if (!summary) {
    return <p>No data available</p>;
  }

  const data = {
    labels: ["Flowrate", "Pressure", "Temperature"],
    datasets: [
      {
        label: "Average Values",
        data: [
          summary.avg_flowrate,
          summary.avg_pressure,
          summary.avg_temperature,
        ],
        backgroundColor: ["#2563eb", "#16a34a", "#dc2626"],
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

export default AvgParametersChart;
