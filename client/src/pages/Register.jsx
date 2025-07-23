import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/userService";

function Register() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await API.post("/register", formData);
      const { token } = res.data;
      localStorage.setItem("token", token);
      navigate("/login"); // o /dashboard si haces login directo
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.message || "Error durante el registro");
    }
  };

  return (
   <div className="flex items-center justify-center min-h-[calc(100vh-160px)] px-4">
      <div className="w-full max-w-2xl bg-white p-12 rounded-lg shadow-lg"> {/* Aumentado a max-w-2xl y p-12 */}
        <h2 className="text-4xl font-bold mb-8 text-center">Registro</h2> {/* Aumentado a text-4xl y mb-8 */}
        {error && <p className="text-red-500 mb-6 text-center text-lg">{error}</p>} {/* Añadido text-lg y mb-6 */}

        <form onSubmit={handleSubmit} className="flex flex-col gap-6"> {/* Aumentado gap a 6 */}
          <input
            type="text"
            name="username"
            placeholder="Usuario"
            value={formData.username}
            onChange={handleChange}
            className="border border-gray-300 p-4 rounded text-lg" /* Aumentado p-4 y text-lg */
            required
          />

          <input
            type="password"
            name="password"
            placeholder="Contraseña"
            value={formData.password}
            onChange={handleChange}
            className="border border-gray-300 p-4 rounded text-lg" /* Aumentado p-4 y text-lg */
            required
          />

          <button
            type="submit"
            className="bg-blue-600 text-white py-4 rounded hover:bg-blue-700 transition text-xl" /* Aumentado py-4 y text-xl */
          >
            Registrarse
          </button>
        </form>
      </div>
    </div>
  );
}

export default Register;
