import React, { useState } from "react";
import taxiImage from "../assets/cuate.svg";

const Suggestions = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: "",
  });

  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Sugerencia enviada:", formData);
    setSubmitted(true);
    setFormData({ name: "", email: "", message: "" });
  };

  return (
    <div className="flex flex-col justify-center items-center min-h-[calc(100vh-128px)] px-4 bg-gray-100 overflow-hidden">
      <div className="max-w-2xl w-full p-6 sm:p-8 bg-white shadow-lg rounded-lg text-center">
        <img
          src={taxiImage}
          alt="Taxi ilustración"
          className="w-28 h-auto mx-auto mb-5"
        />
        <h1 className="text-2xl sm:text-3xl font-bold text-blue-700 mb-2">
          ¿Tienes una sugerencia?
        </h1>
        <p className="text-gray-600 mb-5 text-sm sm:text-base">
          Cuéntanos qué mejorarías o añadirías a TaxiMeter. Tu opinión nos ayuda
          a seguir creciendo. 🚖
        </p>

        {submitted ? (
          <p className="text-green-600 font-semibold text-lg">
            ¡Gracias por tu sugerencia! 📨
          </p>
        ) : (
          <form
            onSubmit={handleSubmit}
            className="flex flex-col gap-3 text-left"
          >
            <input
              type="text"
              name="name"
              placeholder="Tu nombre"
              value={formData.name}
              onChange={handleChange}
              required
              className="border border-gray-300 p-3 rounded w-full"
            />
            <input
              type="email"
              name="email"
              placeholder="Tu correo electrónico"
              value={formData.email}
              onChange={handleChange}
              required
              className="border border-gray-300 p-3 rounded w-full"
            />
            <textarea
              name="message"
              placeholder="Escribe tu sugerencia aquí..."
              value={formData.message}
              onChange={handleChange}
              required
              rows="3"
              className="border border-gray-300 p-3 rounded w-full resize-none"
            />
            <button
              type="submit"
              className="bg-yellow-400 hover:bg-yellow-500 text-black font-bold py-3 rounded mt-2 transition"
            >
              Enviar sugerencia
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

export default Suggestions;
