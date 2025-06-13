
import React, { useState } from "react";

export default function ConsultaItinerarios() {
  const [destino, setDestino] = useState("");
  const [data, setData] = useState("");
  const [porto, setPorto] = useState("");
  const [resultados, setResultados] = useState([]);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState(null);

  async function buscarItinerarios(e) {
    e.preventDefault();
    setLoading(true);
    setErro(null);
    setResultados([]);

    try {
      const params = new URLSearchParams();
      if (destino) params.append("destino", destino);
      if (data) params.append("data", data);
      if (porto) params.append("porto_embarque", porto);

      const res = await fetch(`http://localhost:8000/consulta-itinerarios?${params.toString()}`);
      if (!res.ok) {
        throw new Error(`Erro na consulta: ${res.statusText}`);
      }

      const dados = await res.json();
      setResultados(dados);
    } catch (err) {
      setErro(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Consulta de Itinerários</h2>
      <form onSubmit={buscarItinerarios} style={{ marginBottom: 20 }}>
        <div>
          <label>Destino: </label>
          <input
            type="text"
            value={destino}
            onChange={(e) => setDestino(e.target.value)}
            placeholder="Ex: Ilhas do Caribe"
          />
        </div>
        <div>
          <label>Data (AAAA-MM-DD): </label>
          <input
            type="date"
            value={data}
            onChange={(e) => setData(e.target.value)}
          />
        </div>
        <div>
          <label>Porto de Embarque: </label>
          <input
            type="text"
            value={porto}
            onChange={(e) => setPorto(e.target.value)}
            placeholder="Ex: Rio de Janeiro"
          />
        </div>
        <button type="submit" disabled={loading} style={{ marginTop: 10 }}>
          {loading ? "Buscando..." : "Buscar"}
        </button>
      </form>

      {erro && <p style={{ color: "red" }}>{erro}</p>}

      {resultados.length > 0 && (
        <div>
          <h3>Resultados:</h3>
          <ul>
            {resultados.map((item) => (
              <li key={item.id}>
                <strong>{item.destino}</strong> - Navio: {item.nome_navio} - Noites: {item.noites} - Valor: R$ {item.valor_por_pessoa}<br />
                Portos: {item.portos_embarque}<br />
                Datas disponíveis: {Object.keys(item.datas).join(", ")}<br />
                Lugares visitados: {item.lugares_visitados.join(", ")}
              </li>
            ))}
          </ul>
        </div>
      )}

      {!loading && resultados.length === 0 && <p>Nenhum itinerário encontrado.</p>}
    </div>
  );
}
