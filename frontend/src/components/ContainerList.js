import React, { useEffect, useState } from 'react';

function ContainerList({ onSelect }) {
  const [containers, setContainers] = useState([]);

  useEffect(() => {
    const fetchContainers = async () => {
      const response = await fetch('/api/containers');
      const data = await response.json();
      setContainers(data);
    };
    fetchContainers();
    const interval = setInterval(fetchContainers, 5000); // Poll every 5 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h2 className="text-xl font-bold">Containers</h2>
      <ul>
        {containers.map(container => (
          <li
            key={container.id}
            onClick={() => onSelect(container.id)}
            className="cursor-pointer p-2 hover:bg-gray-200"
          >
            {container.name} - {container.status} - {container.uptime}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ContainerList;
