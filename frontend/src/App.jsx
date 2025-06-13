import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom"
import Home from './home'
import ConsultaItinerarios from "./components/ConsultaForm"

function App() {
  return (
    <BrowserRouter>
      <nav style={{ padding: 10, borderBottom: "1px solid #ccc" }}>
        <Link to="/" style={{ marginRight: 10 }}>Home</Link>
        <Link to="/consulta-itinerarios">Consulta de Itinerários</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/consulta-itinerarios" element={<ConsultaItinerarios />} />
      </Routes>
    </BrowserRouter>
  );
}


export default App;