import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

function MemoryChart({ memoryPercent }) {
  return (
    <div>
      <h3>Memory Usage (%)</h3>
      <LineChart width={400} height={200} data={memoryPercent}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis domain={[0, 100]} />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="value" stroke="#82ca9d" dot={false} isAnimationActive={true} />
      </LineChart>
    </div>
  );
}

export default MemoryChart;
