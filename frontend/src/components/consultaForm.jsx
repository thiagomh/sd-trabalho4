import { useState } from "react";

export default function ItinerariosForm({ onBuscar }) {
    const [destino, setDestino] = useState('');
    const [data, setData] = useState('');
    const [porto, setPorto] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onBuscar({destino, data, porto})
    };

    return (
        <form onSubmit={handleSubmit} >
            <label>
                Destino:
                <input value={destino} onChange={(e) =>
                    setDestino(e.target.value)
                }></input>
            </label>
            <label>
                Data:
                <input type="date" value={data} onChange={(e) =>
                    setData(e.target.value)
                }></input>
            </label>
            <label>
                Porto de Embarque:
                <input value={porto} onChange={(e) =>
                    setPorto(e.target.value)
                }></input>
            </label>
            <button type="submit">Buscar</button>

        </form>
    );
}