import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  const [isOpen, setIsOpen] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav className="bg-blue-600 text-white px-6 py-4">
      <div className="max-w-6xl mx-auto flex justify-between items-center">
        <div className="text-xl font-bold">TaxiMeter</div>

        {/* Botón hamburguesa */}
        <button
          className="md:hidden"
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Toggle menu"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d={isOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"}
            />
          </svg>
        </button>

        {/* Menú en desktop */}
        <div className="hidden md:flex gap-6 items-center">
          <Link to="/" className="hover:underline">
            Inicio
          </Link>
          {!token ? (
            <>
              <Link to="/login" className="hover:underline">
                Login
              </Link>
              <Link to="/register" className="hover:underline">
                Registro
              </Link>
            </>
          ) : (
            <>
              <Link to="/dashboard" className="hover:underline">
                Dashboard
              </Link>
              <button onClick={handleLogout} className="hover:underline">
                Cerrar sesión
              </button>
            </>
          )}
          <Link to="/suggestions" className="hover:underline">
            Sugerencias
          </Link>
        </div>
      </div>

      {/* Menú en mobile */}
      {isOpen && (
        <div className="md:hidden mt-4 space-y-2 px-4">
          <Link to="/" className="block hover:underline">
            Inicio
          </Link>
          {!token ? (
            <>
              <Link to="/login" className="block hover:underline">
                Login
              </Link>
              <Link to="/register" className="block hover:underline">
                Registro
              </Link>
            </>
          ) : (
            <>
              <Link to="/dashboard" className="block hover:underline">
                Dashboard
              </Link>
              <button onClick={handleLogout} className="block hover:underline">
                Cerrar sesión
              </button>
            </>
          )}
          <Link to="/suggestions" className="block hover:underline">
            Sugerencias
          </Link>
        </div>
      )}
    </nav>
  );
}

export default Navbar;
