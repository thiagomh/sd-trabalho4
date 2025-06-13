import { useEffect, useState } from "react";
import { buscarItinerarios } from "../api";
import ItinerariosForm from "./consultaForm";

export default function ItinerariosList() {
    const [itinerarios, setItinerarios] = useState([]);

    const buscar = (filtros = {}) => {
        buscarItinerarios(filtros).then((res) => setItinerarios(res.data));
    };

    useEffect(() => {
        buscar();
    }, []);

    return (
        <div>
            <h2>Itinerários Disponíveis</h2>
            <ItinerariosForm onBuscar={buscar} />
            <ul>
                {itinerarios.length == 0 ? (
                    <li>Nenhum itinerário encontrado.</li>
                ) : (
                    itinerarios.map((item) => (
                        <li key={item.id}>
                            {item.data} - {item.destino}
                        </li>
                    ))
                )}
            </ul>
        </div>
    );
}


