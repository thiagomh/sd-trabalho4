import axios from 'axios';

const API = "http://localhost:8000";

export const buscarItinerarios = (filtros) => 
    axios.get(`${API}/itinerarios`, { params: filtros});

export const reservar = () => axios.get(`${API}/reservas`, data);