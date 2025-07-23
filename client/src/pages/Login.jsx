import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/userService";

function Login() {
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
      const res = await API.post("/login", formData);
      const { token } = res.data;
      localStorage.setItem("token", token);
      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.message || "Error durante el login");
    }
  };
// quiero que el formulario se haga mas grande
  return (
     <div className="flex items-center justify-center min-h-[calc(100vh-160px)] px-4">
      <div className="w-full max-w-2xl bg-white p-12 rounded-lg shadow-lg"> {/* Aumenté max-w-xl a max-w-2xl y p-10 a p-12 */}
        <h2 className="text-4xl font-bold mb-8 text-center">Iniciar sesión</h2> {/* Aumenté text-3xl a text-4xl y mb-6 a mb-8 */}
        {error && <p className="text-red-500 mb-6 text-center text-lg">{error}</p>} {/* Añadí text-lg */}

        <form onSubmit={handleSubmit} className="flex flex-col gap-6"> {/* Aumenté gap-5 a gap-6 */}
          <input
            type="text"
            name="username"
            placeholder="Usuario"
            value={formData.username}
            onChange={handleChange}
            className="border border-gray-300 p-4 rounded text-lg" /* Aumenté p-3 a p-4 y añadí text-lg */
            required
          />

          <input
            type="password"
            name="password"
            placeholder="Contraseña"
            value={formData.password}
            onChange={handleChange}
            className="border border-gray-300 p-4 rounded text-lg" /* Aumenté p-3 a p-4 y añadí text-lg */
            required
          />

          <button
            type="submit"
            className="bg-green-600 text-white py-4 rounded hover:bg-green-700 transition text-xl" /* Aumenté py-3 a py-4 y añadí text-xl */
          >
            Iniciar sesión
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
