import { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/userService';
import { saveTrip, getTrips } from '../services/tripService';

function Dashboard() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  // Estados del viaje
  const [llueve, setLlueve] = useState(false);
  const [evento, setEvento] = useState(false);
  const [maletas, setMaletas] = useState(0);
  const [viajeActivo, setViajeActivo] = useState(false);
  const [enMovimiento, setEnMovimiento] = useState(false);
  const [tiempoParado, setTiempoParado] = useState(0);
  const [tiempoMovimiento, setTiempoMovimiento] = useState(0);
  const [historial, setHistorial] = useState([]);

  const timerRef = useRef(null);

  // Función para cargar historial de viajes
  const fetchTrips = async () => {
    try {
      const res = await getTrips();
      setHistorial(res.data);
    } catch (err) {
      console.error('Error al cargar historial', err);
    }
  };

  // Cargar usuario e historial al montar
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    const fetchUser = async () => {
      try {
        const res = await API.get('/profile');
        setUser(res.data.user);
      } catch (err) {
        console.error('Error al obtener usuario', err);
        localStorage.removeItem('token');
        navigate('/login');
      }
    };

    fetchUser();
    fetchTrips();
  }, [navigate]);

  // Temporizador del taxímetro
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

  // Funciones de control
  const iniciarViaje = () => {
    setTiempoMovimiento(0);
    setTiempoParado(0);
    setViajeActivo(true);
  };

  const finalizarViaje = async () => {
    clearInterval(timerRef.current);
    setViajeActivo(false);

    // Tarifas base
    const tarifaParado = 0.02;
    const tarifaMovimiento = 0.05;
    const precioMaleta = 1.0;

    // Multiplicadores por condiciones
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

      // 🆕 ACTUALIZAR HISTORIAL AUTOMÁTICAMENTE
      fetchTrips();
    } catch (err) {
      console.error('Error al guardar viaje:', err);
      alert('Error al guardar el viaje.');
    }

    // Reiniciar estado
    setLlueve(false);
    setEvento(false);
    setMaletas(0);
    setTiempoMovimiento(0);
    setTiempoParado(0);
  };

  return (
    <div className="max-w-2xl mx-auto mt-10 p-6 bg-white rounded shadow space-y-4">
      <h2 className="text-2xl font-bold">Bienvenido, {user?.username} 👋</h2>

      {/* Controles de condiciones especiales */}
      <div className="flex gap-4">
        <label>
          <input type="checkbox" checked={llueve} onChange={() => setLlueve(!llueve)} />
          <span className="ml-2">¿Está lloviendo? 🌧️</span>
        </label>
        <label>
          <input type="checkbox" checked={evento} onChange={() => setEvento(!evento)} />
          <span className="ml-2">¿Hay evento especial? 🎉</span>
        </label>
      </div>

      {/* Número de maletas */}
      <div>
        <label className="block mb-1">Número de maletas 🧳:</label>
        <input
          type="number"
          value={maletas}
          min={0}
          onChange={(e) => setMaletas(Number(e.target.value))}
          className="border p-2 rounded w-24"
        />
      </div>

      {/* Botones de control */}
      <div className="flex gap-4 mt-4">
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
                enMovimiento ? 'bg-yellow-500 hover:bg-yellow-600' : 'bg-blue-600 hover:bg-blue-700'
              }`}
            >
              {enMovimiento ? 'Parar movimiento' : 'Iniciar movimiento'}
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

      {/* Mostrar tiempos */}
      <div className="mt-4 text-gray-700">
        <p>⏱️ Tiempo en movimiento: {tiempoMovimiento} s</p>
        <p>🛑 Tiempo parado: {tiempoParado} s</p>
      </div>

      {/* Historial de viajes */}
      <div className="mt-6">
        <h3 className="text-xl font-bold mb-2">📜 Historial de viajes</h3>
        {historial.length === 0 ? (
          <p>No hay viajes guardados.</p>
        ) : (
          <ul className="space-y-2">
            {historial.map((trip) => (
              <li key={trip.id} className="border rounded p-3 bg-gray-50">
                <p><strong>🕒 Fecha:</strong> {new Date(trip.timestamp).toLocaleString()}</p>
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
  );
}

export default Dashboard;
