import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

function CpuChart({ cpuPercent }) {
  return (
    <div>
      <h3>CPU Usage (%)</h3>
      <LineChart width={400} height={200} data={cpuPercent}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis domain={[0, 100]} />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="value" stroke="#8884d8" dot={false} isAnimationActive={true} />
      </LineChart>
    </div>
  );
}

export default CpuChart;
