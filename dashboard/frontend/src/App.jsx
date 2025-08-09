import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [services, setServices] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch the list of services from the backend
    axios.get('/services')
      .then((res) => {
        setServices(res.data.services || []);
      })
      .catch((err) => {
        console.error(err);
        setError('Failed to load services');
      });
  }, []);

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-4">Microservice API Factory Dashboard</h1>
      <h2 className="text-xl font-semibold mb-2">Registered Services</h2>
      {error && <div className="text-red-600">{error}</div>}
      {services.length === 0 && !error ? (
        <p>No services registered.</p>
      ) : (
        <ul className="list-disc pl-5 space-y-1">
          {services.map((svc) => (
            <li key={svc}>{svc}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;