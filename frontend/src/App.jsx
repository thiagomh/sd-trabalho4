import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom"
import Home from './home'
import ConsultaForm from "./components/ConsultaForm";
import ReservaForm from "./components/ReservaForm";
import CancelarReservaForm from "./components/CancelarReserva";

function App() {
  return (
    <BrowserRouter>
      <nav style={{ padding: 10, borderBottom: "1px solid #ccc" }}>
        <Link to="/" style={{ marginRight: 10 }}>Home</Link>
        <Link to="/consulta-itinerarios">Consulta de Itinerários </Link>
        <Link to="/reservar">Reservar Cruzeiro </Link>
        <Link to="/cancelar">Cancelar Reserva</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/consulta-itinerarios" element={<ConsultaForm />} />
        <Route path="/reservar" element={<ReservaForm /> } />
        <Route path="/cancelar" element={<CancelarReservaForm />} />
      </Routes>
    </BrowserRouter>
  );
}


export default App;