import React, { useEffect, useState } from 'react';

function Alerts() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const fetchAlerts = async () => {
      const response = await fetch('/api/alerts');
      const data = await response.json();
      setAlerts(data);
    };
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 5000); // Poll every 5 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h2 className="text-xl font-bold">Alerts</h2>
      <ul className="list-disc pl-5">
        {alerts.map((alert, index) => (
          <li key={index} className="text-red-600">
            {alert.timestamp} - {alert.message}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Alerts;
