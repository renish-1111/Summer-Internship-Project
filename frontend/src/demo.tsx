//api data show

import{ useEffect, useState } from 'react';
import axios from 'axios';

export default function Demo() {
  const [data, setData] = useState(null);
  const api = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';  
  useEffect(() => {
    axios.get(`${api}/hello`)
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  return (
    <div>
      {data ? (
        <div>
          <h2>{data}</h2>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}