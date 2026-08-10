import { createContext, useContext, useState } from "react";
import { login as loginRequest } from "../api/auth";

const AuthContext = createContext(null);

// Decodifica o "payload" de um JWT (sem validar assinatura -- só pra exibir
// o nome do usuário na tela; a validação de verdade acontece no backend).
function decodificarUsername(token) {
  try {
    const payloadBase64 = token.split(".")[1];
    const payload = JSON.parse(atob(payloadBase64.replace(/-/g, "+").replace(/_/g, "/")));
    return payload.sub || null;
  } catch {
    return null;
  }
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [username, setUsername] = useState(() => {
    const t = localStorage.getItem("token");
    return t ? decodificarUsername(t) : null;
  });

  async function login(username, password) {
    const accessToken = await loginRequest(username, password);
    localStorage.setItem("token", accessToken);
    setToken(accessToken);
    setUsername(decodificarUsername(accessToken));
  }

  function logout() {
    localStorage.removeItem("token");
    setToken(null);
    setUsername(null);
  }

  return (
    <AuthContext.Provider value={{ token, username, isAuthenticated: !!token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}