import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registrar } from "../api/auth";
import { useAuth } from "../context/AuthContext";
import Nav from "../components/Nav";

export default function Cadastro() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [senha, setSenha] = useState("");
  const [confirmarSenha, setConfirmarSenha] = useState("");
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setErro("");

    if (senha !== confirmarSenha) {
      setErro("As senhas não coincidem.");
      return;
    }
    if (senha.length < 4) {
      setErro("A senha precisa ter pelo menos 4 caracteres.");
      return;
    }

    setCarregando(true);
    try {
      await registrar(username.trim(), senha);
      // já loga automaticamente após cadastrar, pra não precisar digitar de novo
      await login(username.trim(), senha);
      navigate("/");
    } catch (err) {
      if (err.response?.status === 409) {
        setErro("Esse nome de usuário já está em uso.");
      } else {
        setErro(err.response?.data?.detail?.toString() || "Não foi possível cadastrar.");
      }
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
        <h1>Criar conta</h1>

        {erro && <div className="error-msg">{erro}</div>}

        <form onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="username">Usuário</label>
            <input
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoFocus
              minLength={3}
              required
            />
          </div>
          <div className="field">
            <label htmlFor="senha">Senha</label>
            <input
              id="senha"
              type="password"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              minLength={4}
              required
            />
          </div>
          <div className="field">
            <label htmlFor="confirmarSenha">Confirmar senha</label>
            <input
              id="confirmarSenha"
              type="password"
              value={confirmarSenha}
              onChange={(e) => setConfirmarSenha(e.target.value)}
              required
            />
          </div>
          <button className="btn-primary" disabled={carregando}>
            {carregando ? "Criando..." : "Criar conta"}
          </button>
        </form>

        <div className="hint">
          Já tem conta? <Link to="/login">Entrar</Link>
        </div>
      </div>
    </div>
    </div>
  );
}