import { useState } from "react";
import { cancelar } from "../api"; // você já tem essa função na sua API

const CancelarReservaForm = () => {
    const [codigo, setCodigo] = useState("");
    const [mensagem, setMensagem] = useState(null);
    const [erro, setErro] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!codigo.trim()) {
            setErro("Informe o código da reserva.");
            return;
        }

        try {
            const response = await cancelar({ codigo }); // Usando como { params: { codigo } }
            setMensagem(response.data.mensagem || "Reserva cancelada com sucesso.");
            setErro(null);
        } catch (err) {
            console.error("Erro ao cancelar reserva:", err);
            setErro(err.response?.data?.erro || "Erro ao cancelar reserva.");
            setMensagem(null);
        }
    };

    return (
        <div className="max-w-md mx-auto mt-10 p-4 bg-white shadow rounded">
            <h2 className="text-xl font-bold mb-4">Cancelar Reserva</h2>
            <form onSubmit={handleSubmit} className="flex flex-col gap-2">
                <input
                    type="text"
                    placeholder="Código da reserva"
                    value={codigo}
                    onChange={(e) => setCodigo(e.target.value)}
                    className="border p-2 rounded"
                    required
                />
                <button
                    type="submit"
                    className="bg-red-500 text-white py-2 rounded hover:bg-red-600"
                >
                    Cancelar Reserva
                </button>
            </form>

            {mensagem && (
                <div className="mt-4 p-3 bg-green-100 rounded text-green-800">
                    {mensagem}
                </div>
            )}

            {erro && (
                <div className="mt-4 p-3 bg-red-100 rounded text-red-700">
                    {erro}
                </div>
            )}
        </div>
    );
};

export default CancelarReservaForm;
