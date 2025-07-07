// src/components/Register.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/userService';

function Register() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });

  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const res = await API.post('/register', formData);

      const { token } = res.data;
      localStorage.setItem('token', token);

      // Opcional: redirigir directamente al login o a la app
      navigate('/login'); // o navigate('/dashboard') si haces login directo
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.message || 'Error durante el registro');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-bold mb-4">Registro</h2>
      {error && <p className="text-red-500">{error}</p>}

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          type="text"
          name="username"
          placeholder="Usuario"
          value={formData.username}
          onChange={handleChange}
          className="border border-gray-300 p-2 rounded"
          required
        />

        <input
          type="password"
          name="password"
          placeholder="Contraseña"
          value={formData.password}
          onChange={handleChange}
          className="border border-gray-300 p-2 rounded"
          required
        />

        <button
          type="submit"
          className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
        >
          Registrarse
        </button>
      </form>
    </div>
  );
}

export default Register;
