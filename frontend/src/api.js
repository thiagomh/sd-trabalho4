import axios from 'axios';

const API = "http://localhost:8000"; // ms_reserva

export const buscarItinerarios = (filtros) => 
    axios.get(`${API}/consulta-itinerarios`, { params: filtros});

export const reservar = (dados) =>
    axios.post(`${API}/reservar`, dados);

export const cancelar = ({ codigo }) =>
    axios.delete(`${API}/reservar/${codigo}`);