// src/pages/Home.jsx
function Home() {
  return (
    <div className="max-w-3xl mx-auto mt-10 p-6 bg-white rounded shadow">
      <h1 className="text-3xl font-bold mb-4">Bienvenido a TaxiMeter 🚕</h1>
      <p className="text-lg text-gray-700">
        Esta aplicación te permite calcular automáticamente tarifas de taxi basadas en tiempo de espera, movimiento, condiciones especiales como lluvia o eventos, y mucho más.
      </p>
      <p className="mt-4 text-gray-600">
        Regístrate o inicia sesión para comenzar a usar el taxímetro digital.
      </p>
    </div>
  );
}

export default Home;
