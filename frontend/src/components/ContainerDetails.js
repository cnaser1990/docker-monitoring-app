import React, { useEffect, useState } from 'react';
import CpuChart from './CpuChart';
import MemoryChart from './MemoryChart';
import LogViewer from './LogViewer';

function ContainerDetails({ containerId }) {
  const [cpuData, setCpuData] = useState([]);
  const [memoryData, setMemoryData] = useState([]);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch(`/api/containers/${containerId}/stats`);
        const data = await response.json();
        const now = new Date().toLocaleTimeString();

        console.log('Fetched stats:', data); // ✅ log to check

        setCpuData(prev => [...prev.slice(-19), { name: now, value: data.cpu_percent }]);
        setMemoryData(prev => [...prev.slice(-19), { name: now, value: data.memory_percent }]);
      } catch (error) {
        console.error('Failed to fetch stats', error);
      }
    };

    fetchStats();
    const interval = setInterval(fetchStats, 5000); // Poll every 5 seconds
    return () => clearInterval(interval);
  }, [containerId]);

  return (
    <div>
      <h2 className="text-xl font-bold">Container Details</h2>
      <div className="flex">
        <CpuChart cpuPercent={cpuData.length ? cpuData : [{ name: '', value: 0 }]} />
        <MemoryChart memoryPercent={memoryData.length ? memoryData : [{ name: '', value: 0 }]} />
      </div>
      <LogViewer containerId={containerId} />
    </div>
  );
}

export default ContainerDetails;
