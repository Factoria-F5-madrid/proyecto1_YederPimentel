import { useEffect, useState } from "react";
import taxiImage from "../assets/cuate.svg";
import backgroundMap from "../assets/map.svg"; // imagen de fondo decorativa

function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsLoggedIn(!!token);
  }, []);

  return (
    <div
      className="max-w-4xl w-full p-8 rounded-lg shadow-lg text-center bg-white bg-no-repeat bg-top bg-contain"
      style={{
        backgroundImage: `url(${backgroundMap})`,
        backgroundPosition: "center top",
        backgroundRepeat: "no-repeat",
        backgroundSize: "100% auto",
      }}
    >
      {/* Imagen SVG del taxi */}
      <img src={taxiImage} alt="Taxi" className="w-48 h-auto mx-auto mb-8" />

      {/* Título */}
      <h1 className="text-4xl font-bold text-yellow-500 mb-4">
        Bienvenido a TaxiMeter F5 🚖
      </h1>

      {/* Texto descriptivo */}
      <p className="text-lg text-gray-900 mb-4 leading-relaxed">
        TaxiMeter es tu asistente digital para calcular tarifas de taxi en
        tiempo real. Controla los segundos que tu taxi pasa detenido o en
        movimiento, añade recargos por maletas, condiciones meteorológicas o
        eventos especiales, y obtén un recibo claro y transparente al finalizar
        el trayecto.
      </p>

      <p className="text-lg text-gray-900 mb-4 leading-relaxed">
        Nuestra plataforma está pensada para ser fácil de usar, rápida y
        accesible desde cualquier dispositivo. Tanto si eres un taxista
        profesional como si estás desarrollando una app educativa, esta
        herramienta te ahorrará tiempo y te permitirá concentrarte en lo que
        importa: el trayecto.
      </p>

      {!isLoggedIn && (
        <p className="text-md text-gray-800 mt-6 font-medium">
          Regístrate o inicia sesión para comenzar a usar el taxímetro digital.
        </p>
      )}
    </div>
  );
}

export default Home;
