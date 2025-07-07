// src/pages/Dashboard.jsx
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/userService';

function Dashboard() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    // Obtener datos del usuario autenticado
    const fetchUser = async () => {
      try {
        const res = await API.get('/profile'); // Endpoint protegido en Flask
        setUser(res.data.user);
      } catch (err) {
        console.error('Error al obtener usuario', err);
        localStorage.removeItem('token');
        navigate('/login');
      }
    };

    fetchUser();
  }, [navigate]);

  return (
    <div className="max-w-2xl mx-auto mt-10 p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-bold mb-4">Bienvenido al Dashboard</h2>
      {user ? (
        <p className="text-lg">Hola, <span className="font-semibold">{user.username}</span> 👋</p>
      ) : (
        <p>Cargando usuario...</p>
      )}
    </div>
  );
}

export default Dashboard;
