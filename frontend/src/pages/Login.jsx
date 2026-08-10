import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Nav from "../components/Nav";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setErro("");
    setCarregando(true);
    try {
      await login(username, password);
      navigate("/");
    } catch {
      setErro("Usuário ou senha inválidos.");
    } finally {
      setCarregando(false);
    }
  }

  return (
    <div className="shell">
      <Nav />
    <div className="login-screen">
      <div className="login-card">
        <div className="eyebrow">RestAPIFurb</div>
        <h1>Controle de patrimônio</h1>

        {erro && <div className="error-msg">{erro}</div>}

        <form onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="username">Usuário</label>
            <input
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoFocus
              required
            />
          </div>
          <div className="field">
            <label htmlFor="password">Senha</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button className="btn-primary" disabled={carregando}>
            {carregando ? "Entrando..." : "Entrar"}
          </button>
        </form>

        <div className="hint">
          usuário de teste (seed.py): admin / admin123
        </div>

        <div className="hint" style={{ marginTop: 10 }}>
          Não tem conta? <Link to="/cadastro">Cadastre-se</Link>
        </div>
      </div>
    </div>
    </div>
  );
}