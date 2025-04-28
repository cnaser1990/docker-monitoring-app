import React, { useEffect, useState } from 'react';

function LogViewer({ containerId }) {
  const [logs, setLogs] = useState('');

  useEffect(() => {
    const fetchLogs = async () => {
      const response = await fetch(`/api/containers/${containerId}/logs`);
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        setLogs(prev => prev + chunk);
      }
    };
    setLogs(''); // Reset logs when container changes
    fetchLogs();
  }, [containerId]);

  return (
    <div>
      <h3 className="text-lg font-semibold">Logs</h3>
      <pre className="bg-gray-800 text-white p-4 rounded" style={{ height: '300px', overflow: 'auto' }}>
        {logs}
      </pre>
    </div>
  );
}

export default LogViewer;
