import { useEffect, useState } from "react";
import Nav from "../components/Nav";
import { useAuth } from "../context/AuthContext";
import { listarUsuarios, removerUsuario } from "../api/usuarios";

export default function Usuarios() {
  const { username: usuarioLogado } = useAuth();

  const [usuarios, setUsuarios] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  async function carregar() {
    setCarregando(true);
    setErro("");
    try {
      const data = await listarUsuarios();
      setUsuarios(data);
    } catch {
      setErro("Não foi possível carregar os usuários.");
    } finally {
      setCarregando(false);
    }
  }

  useEffect(() => {
    carregar();
  }, []);

  async function handleRemover(usuario) {
    if (usuario.username === usuarioLogado) {
      // o backend também bloqueia isso, mas evitamos a chamada desnecessária
      alert("Você não pode remover o próprio usuário logado.");
      return;
    }
    if (!confirm(`Remover o usuário "${usuario.username}"?`)) return;

    try {
      await removerUsuario(usuario.id);
      await carregar();
    } catch (err) {
      setErro(err.response?.data?.detail?.toString() || "Não foi possível remover o usuário.");
    }
  }

  return (
    <div className="shell">
      <Nav />
      <main className="content">
        <div className="page-header">
          <div>
            <h1>Usuários</h1>
            <p>Contas com acesso ao cadastro de equipamentos</p>
          </div>
        </div>

        {erro && <div className="error-msg">{erro}</div>}

        {carregando ? (
          <p className="loading">Carregando usuários...</p>
        ) : usuarios.length === 0 ? (
          <div className="empty-state">Nenhum usuário cadastrado.</div>
        ) : (
          <table className="users-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Usuário</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {usuarios.map((u) => (
                <tr key={u.id}>
                  <td className="mono">#{String(u.id).padStart(4, "0")}</td>
                  <td>
                    {u.username}
                    {u.username === usuarioLogado && <span className="you-badge">você</span>}
                  </td>
                  <td className="table-actions">
                    <button
                      className="danger"
                      disabled={u.username === usuarioLogado}
                      onClick={() => handleRemover(u)}
                    >
                      Remover
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </main>
    </div>
  );
}