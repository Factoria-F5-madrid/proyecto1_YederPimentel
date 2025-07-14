import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/userService";
import { saveTrip, getTrips } from "../services/tripService";
import taxiImage from "../assets/cuate.svg"; // Asegúrate de tener la imagen

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

      alert(`✅ Recibo guardado. Tarifa total: ${totalCalculado} €`);
      fetchTrips();
    } catch (err) {
      console.error("Error al guardar viaje:", err);
      alert("Error al guardar el viaje.");
    }

    setLlueve(false);
    setEvento(false);
    setMaletas(0);
    setTiempoMovimiento(0);
    setTiempoParado(0);
  };

  return (
    <div className="min-h-[calc(100vh-128px)] flex justify-center items-start px-4 py-10 bg-white">
      <div className="w-full max-w-5xl bg-white rounded-lg shadow-lg p-8">
        {/* Encabezado */}
        <div className="flex flex-col sm:flex-row justify-between items-center gap-6 mb-8">
          <div>
            <h2 className="text-3xl font-bold text-blue-700">
              ¡Hola, {user?.username}! 👋
            </h2>
            <p className="text-gray-600 mt-2">
              Controla tu taxímetro en tiempo real y guarda tus trayectos.
            </p>
          </div>
          <img
            src={taxiImage}
            alt="Taxi ilustración"
            className="w-32 sm:w-40 md:w-48"
          />
        </div>

        {/* Controles */}
        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <div className="space-y-4">
            <div className="flex items-center gap-4">
              <label>
                <input
                  type="checkbox"
                  checked={llueve}
                  onChange={() => setLlueve(!llueve)}
                />
                <span className="ml-2">¿Llueve? 🌧️</span>
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={evento}
                  onChange={() => setEvento(!evento)}
                />
                <span className="ml-2">¿Evento especial? 🎉</span>
              </label>
            </div>

            <div>
              <label className="block mb-1">Maletas 🧳:</label>
              <input
                type="number"
                value={maletas}
                min={0}
                onChange={(e) => setMaletas(Number(e.target.value))}
                className="border border-gray-300 p-2 rounded w-24"
              />
            </div>

            {/* Botones */}
            <div className="flex gap-4 flex-wrap">
              {!viajeActivo ? (
                <button
                  onClick={iniciarViaje}
                  className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
                >
                  Iniciar viaje
                </button>
              ) : (
                <>
                  <button
                    onClick={() => setEnMovimiento(!enMovimiento)}
                    className={`px-4 py-2 rounded text-white ${
                      enMovimiento
                        ? "bg-yellow-500 hover:bg-yellow-600"
                        : "bg-blue-600 hover:bg-blue-700"
                    }`}
                  >
                    {enMovimiento ? "Parar movimiento" : "Iniciar movimiento"}
                  </button>
                  <button
                    onClick={finalizarViaje}
                    className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
                  >
                    Finalizar viaje
                  </button>
                </>
              )}
            </div>

            <div className="text-gray-700 mt-4">
              <p>⏱️ Movimiento: {tiempoMovimiento} s</p>
              <p>🛑 Parado: {tiempoParado} s</p>
            </div>
          </div>

          {/* Historial de viajes */}
          <div>
            <h3 className="text-xl font-bold mb-2">📜 Historial</h3>
            {historial.length === 0 ? (
              <p className="text-gray-500">No hay viajes registrados aún.</p>
            ) : (
              <ul className="space-y-2 max-h-72 overflow-y-auto pr-2">
                {historial.map((trip) => (
                  <li
                    key={trip.id}
                    className="border border-gray-300 rounded p-3 bg-gray-50"
                  >
                    <p>
                      <strong>🕒</strong>{" "}
                      {new Date(trip.timestamp).toLocaleString()}
                    </p>
                    <p>🛑 Parado: {trip.stopped_time}s</p>
                    <p>🚗 Movimiento: {trip.moving_time}s</p>
                    <p>🧳 Maletas: {trip.suitcase_count}</p>
                    <p>💰 Total: {trip.total} €</p>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
