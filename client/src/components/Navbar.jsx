// src/components/Navbar.jsx
import { Link, useNavigate } from 'react-router-dom';

function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <nav className="bg-blue-600 text-white px-6 py-4 flex justify-between items-center">
      <div className="text-xl font-bold">TaxiMeter</div>
      <div className="flex gap-4 items-center">
        <Link to="/" className="hover:underline">Inicio</Link>
        {!token ? (
          <>
            <Link to="/login" className="hover:underline">Login</Link>
            <Link to="/register" className="hover:underline">Registro</Link>
          </>
        ) : (
          <>
            <Link to="/dashboard" className="hover:underline">Dashboard</Link>
            <button onClick={handleLogout} className="hover:underline">Cerrar sesión</button>
          </>
        )}
        <Link to="/sugerencias" className="hover:underline">Sugerencias</Link>
      </div>
    </nav>
  );
}

export default Navbar;
