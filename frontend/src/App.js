import React, { useState } from 'react';
import ContainerList from './components/ContainerList';
import ContainerDetails from './components/ContainerDetails';
import Alerts from './components/Alerts';

function App() {
  const [selectedContainer, setSelectedContainer] = useState(null);

  return (
    <div className="flex" style={{height:"100vh"}}>
      <div className="w-1/4 p-4 " style={{backgroundColor:"rgba(0, 31, 198, 0.33)"}}>
        <ContainerList onSelect={setSelectedContainer} />
      </div>
      <div className="w-3/4 p-4">
        {selectedContainer && <ContainerDetails containerId={selectedContainer} />}
        <Alerts />
      </div>
    </div>
  );
}

export default App;

