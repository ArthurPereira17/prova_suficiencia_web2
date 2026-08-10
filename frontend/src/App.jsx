import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import RotaProtegida from "./components/RotaProtegida";
import Login from "./pages/Login";
import Cadastro from "./pages/Cadastro";
import Equipamentos from "./pages/Equipamentos";
import Usuarios from "./pages/Usuarios";

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Pública: sem login só dá pra ver Equipamentos */}
          <Route path="/" element={<Equipamentos />} />

          <Route path="/login" element={<Login />} />
          <Route path="/cadastro" element={<Cadastro />} />

          {/* Protegida: só aparece depois de logar */}
          <Route
            path="/usuarios"
            element={
              <RotaProtegida>
                <Usuarios />
              </RotaProtegida>
            }
          />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}