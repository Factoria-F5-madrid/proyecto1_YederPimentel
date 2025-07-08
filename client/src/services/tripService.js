// src/services/tripService.js
import axios from 'axios';

// Crear instancia Axios para trips
const APITRIP = axios.create({
  baseURL: 'http://localhost:5000/api/trips',
});

// Añadir token JWT automáticamente
APITRIP.interceptors.request.use((req) => {
  const token = localStorage.getItem('token');
  if (token) {
    req.headers.Authorization = `Bearer ${token}`;
  }
  return req;
});

// Función para guardar un viaje
export const saveTrip = async (tripData) => {
  return await APITRIP.post('/trip', tripData);
};

export const getTrips = async () => {
  return await APITRIP.get('/trip');
};
// Puedes agregar más funciones aquí si quieres como:
// getTrips(), deleteTrip(id), etc.
0