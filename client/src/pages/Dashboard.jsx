import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/userService";
import { saveTrip, getTrips } from "../services/tripService";
import taxiImage from "../assets/cuate.svg";

function Dashboard() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  const [llueve, setLlueve] = useState(false);
  const [evento, setEvento] = useState(false);
  const [maletas, setMaletas] = useState(0);
  const [viajeActivo, setViajeActivo] = useState(false);
  const [enMovimiento, setEnMovimiento] = useState(false);
  const [tiempoParado, setTiempoParado] = useState(0);
  const [tiempoMovimiento, setTiempoMovimiento] = useState(0);
  const [historial, setHistorial] = useState([]);

  const timerRef = useRef(null);

  const fetchTrips = async () => {
    try {
      const res = await getTrips();
      setHistorial(res.data);
    } catch (err) {
      console.error("Error al cargar historial", err);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }

    const fetchUser = async () => {
      try {
        const res = await API.get("/profile");
        setUser(res.data.user);
      } catch (err) {
        console.error("Error al obtener usuario", err);
        localStorage.removeItem("token");
        navigate("/login");
      }
    };

    fetchUser();
    fetchTrips();
  }, [navigate]);

  useEffect(() => {
    if (viajeActivo) {
      timerRef.current = setInterval(() => {
        if (enMovimiento) {
          setTiempoMovimiento((prev) => prev + 1);
        } else {
          setTiempoParado((prev) => prev + 1);
        }
      }, 1000);
    }

    return () => clearInterval(timerRef.current);
  }, [viajeActivo, enMovimiento]);

  const iniciarViaje = () => {
    setTiempoMovimiento(0);
    setTiempoParado(0);
    setViajeActivo(true);
  };

  const finalizarViaje = async () => {
    clearInterval(timerRef.current);
    setViajeActivo(false);

    const tarifaParado = 0.02;
    const tarifaMovimiento = 0.05;
    const precioMaleta = 1.0;

    let multiplicador = 1;
    if (llueve) multiplicador *= 1.5;
    if (evento) multiplicador *= 2;

    const totalCalculado = (
      (tiempoParado * tarifaParado +
        tiempoMovimiento * tarifaMovimiento +
        maletas * precioMaleta) *
      multiplicador
    ).toFixed(2);

    try {
      await saveTrip({
        stopped_time: tiempoParado,
        moving_time: tiempoMovimiento,
        suitcase_count: maletas,
        total: totalCalculado,
      });

      // Notificación más elegante
      const notification = document.createElement("div");
      notification.className = "fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg animate-fade-in z-50";
      notification.innerHTML = `✅ Viaje guardado! <strong>${totalCalculado} €</strong>`;
      document.body.appendChild(notification);
      
      setTimeout(() => {
        notification.classList.remove("animate-fade-in");
        notification.classList.add("animate-fade-out");
        setTimeout(() => notification.remove(), 500);
      }, 3000);

      fetchTrips();
    } catch (err) {
      console.error("Error al guardar viaje:", err);
      const errorNotif = document.createElement("div");
      errorNotif.className = "fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg animate-fade-in z-50";
      errorNotif.textContent = "❌ Error al guardar el viaje";
      document.body.appendChild(errorNotif);
      
      setTimeout(() => {
        errorNotif.classList.remove("animate-fade-in");
        errorNotif.classList.add("animate-fade-out");
        setTimeout(() => errorNotif.remove(), 500);
      }, 3000);
    }

    setLlueve(false);
    setEvento(false);
    setMaletas(0);
    setTiempoMovimiento(0);
    setTiempoParado(0);
  };

  return (
    <div className="min-h-[calc(100vh-80px)] bg-gradient-to-br from-blue-50 to-gray-50 py-3 px-3 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
      
        <div className="flex flex-col md:flex-row justify-between items-center gap-8 mb-4 p-2 bg-white rounded-xl shadow-md">
          <div>
            <h1 className="text-4xl pl-8 font-extrabold text-gray-900 mb-2">
              ¡Bienvenido, <span className="text-blue-600">{user?.username}</span>!
            </h1>
            <p className="text-lg pl-8 text-gray-600">
              Controla tus viajes con el taxímetro inteligente
            </p>
          </div>
          <img 
            src={taxiImage} 
            alt="Taxi ilustración" 
            className="w-48 md:w-32 pr-8 transition-transform hover:scale-105" 
          />
        </div>

        
        <div className="grid lg:grid-cols-3 gap-8">
        
          <div className="lg:col-span-2 bg-white p-2 rounded-xl shadow-md">
            <h2 className="text-2xl font-bold text-gray-800 mb-2 pb-2 border-b border-gray-200">
              🚖 Control del Taxímetro
            </h2>

          
            <div className="space-y-6">
              {/* Factores multiplicadores */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div 
                  className={`p-4 rounded-lg border-2 transition-all ${llueve ? 'border-blue-300 bg-blue-50' : 'border-gray-200'}`}
                  onClick={() => setLlueve(!llueve)}
                >
                  <label className="flex items-center space-x-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={llueve}
                      onChange={() => {}}
                      className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
                    />
                    <span className="text-gray-700 font-medium">
                      Lluvia 🌧️ <span className="text-sm text-gray-500">(+50%)</span>
                    </span>
                  </label>
                </div>

                <div 
                  className={`p-4 rounded-lg border-2 transition-all ${evento ? 'border-purple-300 bg-purple-50' : 'border-gray-200'}`}
                  onClick={() => setEvento(!evento)}
                >
                  <label className="flex items-center space-x-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={evento}
                      onChange={() => {}}
                      className="h-5 w-5 text-purple-600 rounded focus:ring-purple-500"
                    />
                    <span className="text-gray-700 font-medium">
                      Evento especial 🎉 <span className="text-sm text-gray-500">(+100%)</span>
                    </span>
                  </label>
                </div>
              </div>

              {/* Selector de maletas */}
              <div className="bg-gray-50 p-5 rounded-lg">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Número de maletas 🧳
                </label>
                <div className="flex items-center">
                  <button 
                    onClick={() => setMaletas(Math.max(0, maletas - 1))}
                    className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-l"
                  >
                    -
                  </button>
                  <div className="bg-white py-2 px-6 border-t border-b border-gray-300 text-center font-medium">
                    {maletas}
                  </div>
                  <button 
                    onClick={() => setMaletas(maletas + 1)}
                    className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-r"
                  >
                    +
                  </button>
                </div>
              </div>

              {/* Temporizadores */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-blue-800">Tiempo en movimiento</span>
                    <span className="text-2xl font-bold text-blue-600">🚗</span>
                  </div>
                  <div className="text-3xl font-bold text-blue-700 mt-2">
                    {tiempoMovimiento}s
                  </div>
                </div>

                <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-100">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-yellow-800">Tiempo parado</span>
                    <span className="text-2xl font-bold text-yellow-600">🛑</span>
                  </div>
                  <div className="text-3xl font-bold text-yellow-700 mt-2">
                    {tiempoParado}s
                  </div>
                </div>
              </div>

              {/* Botones de acción */}
              <div className="flex flex-wrap gap-4 pt-4">
                {!viajeActivo ? (
                  <button
                    onClick={iniciarViaje}
                    className="flex-1 bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg shadow-md hover:shadow-lg transition-all duration-300 flex items-center justify-center space-x-2"
                  >
                    <span>▶️</span>
                    <span>Iniciar viaje</span>
                  </button>
                ) : (
                  <>
                    <button
                      onClick={() => setEnMovimiento(!enMovimiento)}
                      className={`flex-1 font-bold py-3 px-6 rounded-lg shadow-md hover:shadow-lg transition-all duration-300 flex items-center justify-center space-x-2 ${
                        enMovimiento
                          ? "bg-yellow-500 hover:bg-yellow-600 text-white"
                          : "bg-blue-600 hover:bg-blue-700 text-white"
                      }`}
                    >
                      <span>{enMovimiento ? "🛑" : "🚗"}</span>
                      <span>{enMovimiento ? "Detener" : "Mover"}</span>
                    </button>
                    <button
                      onClick={finalizarViaje}
                      className="flex-1 bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-6 rounded-lg shadow-md hover:shadow-lg transition-all duration-300 flex items-center justify-center space-x-2"
                    >
                      <span>⏹️</span>
                      <span>Finalizar viaje</span>
                    </button>
                  </>
                )}
              </div>
            </div>
          </div>

          {/* Historial */}
          <div className="bg-white p-6 rounded-xl shadow-md">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 pb-2 border-b border-gray-200">
              📋 Historial de Viajes
            </h2>

            {historial.length === 0 ? (
              <div className="text-center py-8">
                <div className="text-gray-400 mb-4 text-6xl">🧐</div>
                <p className="text-gray-500">No hay viajes registrados aún</p>
              </div>
            ) : (
              <div className="space-y-4 max-h-[600px] overflow-y-auto pr-2">
                {historial.map((trip) => (
                  <div 
                    key={trip.id} 
                    className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <span className="text-sm font-medium text-gray-500">
                        {new Date(trip.timestamp).toLocaleString()}
                      </span>
                      <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded">
                        {trip.total} €
                      </span>
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div className="flex items-center space-x-1">
                        <span>🛑</span>
                        <span>{trip.stopped_time}s</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <span>🚗</span>
                        <span>{trip.moving_time}s</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <span>🧳</span>
                        <span>{trip.suitcase_count}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <span>💰</span>
                        <span>{trip.total} €</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;