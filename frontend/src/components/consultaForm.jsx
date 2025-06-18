import React, { useState } from 'react';
import { buscarItinerarios } from '../api';

const ConsultaForm = () => {
  const [filtros, setFiltros] = useState({
    destino: '',
    data_embarque: '',
    porto_embarque: '',
  });

  const [resultados, setResultados] = useState([]);

  const handleChange = (e) => {
    setFiltros({ ...filtros, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResultados([]); 
    try {
      const response = await buscarItinerarios(filtros);
      setResultados(response.data);
    } catch (error) {
      console.error('Erro ao buscar itinerários:', error);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Consulta de Itinerários</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="destino"
          placeholder="Destino"
          value={filtros.destino}
          onChange={handleChange}
        />
        <input
          type="date"
          name="data_embarque"
          value={filtros.data_embarque}
          onChange={handleChange}
        />
        <input
          type="text"
          name="porto_embarque"
          placeholder="Porto de Embarque"
          value={filtros.porto_embarque}
          onChange={handleChange}
        />
        <button type="submit">Buscar</button>
      </form>

      <div style={{ marginTop: '20px' }}>
        {resultados.length === 0 ? (
          <p>Nenhum itinerário encontrado.</p>
        ) : (
          resultados.map((itinerario, index) => (
            <div key={index} style={{ border: '1px solid #ccc', margin: '10px 0', padding: '10px' }}>
              <h3>{itinerario.nome_navio}</h3>
              <p><strong>Destino:</strong> {itinerario.destino}</p>
              <p><strong>Porto de Embarque:</strong> {itinerario.portos_embarque}</p>
              <p><strong>Data:</strong> {itinerario.data}</p>
              <p><strong>Noites:</strong> {itinerario.noites}</p>
              <p><strong>Valor por Pessoa:</strong> R$ {itinerario.valor_por_pessoa}</p>
              <p><strong>Cabines Disponíveis:</strong> {itinerario.cabines_disponiveis}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default ConsultaForm;
