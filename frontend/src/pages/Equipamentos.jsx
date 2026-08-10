import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import Nav from "../components/Nav";
import {
  listarEquipamentos,
  criarEquipamento,
  atualizarEquipamento,
  removerEquipamento,
} from "../api/equipamentos";
import { listarTipos } from "../api/tipos";

const FORM_VAZIO = { nome: "", tipo_id: "" };

export default function Equipamentos() {
  const { isAuthenticated } = useAuth();

  const [equipamentos, setEquipamentos] = useState([]);
  const [tipos, setTipos] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  const [form, setForm] = useState(FORM_VAZIO);
  const [editandoId, setEditandoId] = useState(null);
  const [salvando, setSalvando] = useState(false);

  async function carregarTudo() {
    setCarregando(true);
    setErro("");
    try {
      const [eqs, tps] = await Promise.all([listarEquipamentos(), listarTipos()]);
      setEquipamentos(eqs);
      setTipos(tps);
    } catch {
      setErro("Não foi possível carregar os dados. A API está rodando em localhost:8080?");
    } finally {
      setCarregando(false);
    }
  }

  useEffect(() => {
    carregarTudo();
  }, []);

  function iniciarEdicao(equipamento) {
    setEditandoId(equipamento.id);
    setForm({ nome: equipamento.nome, tipo_id: String(equipamento.tipo.id) });
  }

  function cancelarEdicao() {
    setEditandoId(null);
    setForm(FORM_VAZIO);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!form.nome.trim() || !form.tipo_id) return;

    setSalvando(true);
    setErro("");
    try {
      const payload = { nome: form.nome.trim(), tipo_id: Number(form.tipo_id) };
      if (editandoId) {
        await atualizarEquipamento(editandoId, payload);
      } else {
        await criarEquipamento(payload);
      }
      cancelarEdicao();
      await carregarTudo();
    } catch (err) {
      setErro(err.response?.data?.detail?.toString() || "Não foi possível salvar o equipamento.");
    } finally {
      setSalvando(false);
    }
  }

  async function handleRemover(id) {
    if (!confirm("Remover este equipamento?")) return;
    try {
      await removerEquipamento(id);
      await carregarTudo();
    } catch {
      setErro("Não foi possível remover o equipamento.");
    }
  }

  return (
    <div className="shell">
      <Nav />

      <main className="content">
        <div className="page-header">
          <div>
            <h1>Equipamentos</h1>
            <p>Cadastro consumindo a API REST em localhost:8080/RestAPIFurb</p>
          </div>
        </div>

        {erro && <div className="error-msg">{erro}</div>}

        {!isAuthenticated && (
          <div className="hint" style={{ marginBottom: 20 }}>
            Você está vendo os equipamentos como visitante. Entre para poder adicionar, editar
            ou remover.
          </div>
        )}

        {isAuthenticated && (
          <form className="equip-form" onSubmit={handleSubmit}>
            <div className="field">
              <label htmlFor="nome">Nome do equipamento</label>
              <input
                id="nome"
                value={form.nome}
                onChange={(e) => setForm({ ...form, nome: e.target.value })}
                placeholder="Ex: Notebook Dell"
                required
              />
            </div>
            <div className="field">
              <label htmlFor="tipo">Tipo</label>
              <select
                id="tipo"
                value={form.tipo_id}
                onChange={(e) => setForm({ ...form, tipo_id: e.target.value })}
                required
                style={{
                  width: "100%",
                  padding: "10px 12px",
                  border: "1px solid var(--line)",
                  borderRadius: "6px",
                  fontSize: "0.95rem",
                  background: "#fbfcfc",
                }}
              >
                <option value="" disabled>
                  Selecione...
                </option>
                {tipos.map((t) => (
                  <option key={t.id} value={t.id}>
                    {t.nome}
                  </option>
                ))}
              </select>
            </div>
            <button className="btn-primary" disabled={salvando}>
              {salvando ? "Salvando..." : editandoId ? "Salvar alterações" : "Adicionar"}
            </button>
            {editandoId && (
              <button type="button" className="btn-ghost" onClick={cancelarEdicao}>
                Cancelar
              </button>
            )}
          </form>
        )}

        {carregando ? (
          <p className="loading">Carregando equipamentos...</p>
        ) : equipamentos.length === 0 ? (
          <div className="empty-state">Nenhum equipamento cadastrado ainda.</div>
        ) : (
          <div className="equip-grid">
            {equipamentos.map((eq) => (
              <div className="equip-card" key={eq.id}>
                <span className="tag-id">#{String(eq.id).padStart(4, "0")}</span>
                <h3>{eq.nome}</h3>
                <span className="badge">{eq.tipo.nome}</span>
                {isAuthenticated && (
                  <div className="actions">
                    <button onClick={() => iniciarEdicao(eq)}>Editar</button>
                    <button className="danger" onClick={() => handleRemover(eq.id)}>
                      Remover
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}