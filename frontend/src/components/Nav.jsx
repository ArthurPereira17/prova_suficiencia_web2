import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Nav() {
  const { isAuthenticated, username, logout } = useAuth();

  return (
    <header className="topbar">
      <div className="topbar-left">
        <div className="brand">
          RestAPIFurb <small>Patrimônio</small>
        </div>
        <nav className="topnav">
          <NavLink to="/" end className={({ isActive }) => (isActive ? "active" : "")}>
            Equipamentos
          </NavLink>
          {isAuthenticated && (
            <NavLink to="/usuarios" className={({ isActive }) => (isActive ? "active" : "")}>
              Usuários
            </NavLink>
          )}
        </nav>
      </div>

      <div className="topbar-right">
        {isAuthenticated ? (
          <>
            <span className="current-user">{username}</span>
            <button onClick={logout}>Sair</button>
          </>
        ) : (
          <>
            <NavLink to="/login" className="topbar-link">
              Entrar
            </NavLink>
            <NavLink to="/cadastro" className="topbar-link">
              Cadastrar
            </NavLink>
          </>
        )}
      </div>
    </header>
  );
}