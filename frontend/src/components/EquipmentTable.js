function EquipmentTable({ data }) {
  return (
    <table border="1">
      <thead>
        <tr>
          <th>Name</th>
          <th>Type</th>
          <th>Flowrate</th>
          <th>Pressure</th>
          <th>Temperature</th>
        </tr>
      </thead>
      <tbody>
        {data.map((e, i) => (
          <tr key={i}>
            <td>{e.equipment_name}</td>
            <td>{e.equipment_type}</td>
            <td>{e.flowrate}</td>
            <td>{e.pressure}</td>
            <td>{e.temperature}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default EquipmentTable;
