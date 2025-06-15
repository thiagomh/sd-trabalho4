import { useState } from "react";
import { reservar } from "../api";

const ReservaForm = () => {
    const [dados, setDados] = useState({
        nome_navio: '',
        destino: '',
        data_embarque: '',
        qtd_cabines: 1,
        qtd_passageiros: 1,
    });

    const [resposta, setResposta] = useState(null);
    const [erro, setErro] = useState(null);

    const handleChange = (e) => {
        const { name, value, type } = e.target;
        setDados({ ...dados, 
            [name]: type === "number" ? parseInt(value, 10) : value 
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            console.log("Enviando dados:", dados);
            const response = await reservar(dados);
            setResposta(response.data)
        } catch (error) {
            console.error('Erro ao criar reserva: ', error)
        }
    };

    return (
        <div className="max-w-md mx-auto mt-10 p-4 bg-white shadow rounded">
            <h2 className="text-xl font-bold mb-4">Reservar Cruzeiro</h2>
            <form onSubmit={handleSubmit} className="flex flex-col gap-2">
                <input type="text" name="nome_navio" placeholder="Nome do navio" required onChange={handleChange} />
                <input type="text" name="destino" placeholder="Destino" required onChange={handleChange} />
                <input type="date" name="data_embarque" required onChange={handleChange} />
                <input type="number" name="qtd_passageiros" placeholder="Passageiros" min={1} required onChange={handleChange} />
                <input type="number" name="qtd_cabines" placeholder="Cabines" min={1} required onChange={handleChange} />
                <button type="submit" className="bg-blue-500 text-white py-2 rounded">Reservar</button>
            </form>

            {resposta && (
                <div className="mt-4 p-3 bg-green-100 rounded">
                <p><strong>ID da Reserva:</strong> {resposta.reserva_id}</p>
                <p><strong>Valor Total:</strong> R$ {resposta.valor_total}</p>
                <a href={resposta.link_pagamento} target="_blank" className="text-blue-600 underline">Pagar agora</a>
                </div>
            )}

            {erro && <p className="mt-4 text-red-500">{erro}</p>}
        </div>
    );
};

export default ReservaForm;