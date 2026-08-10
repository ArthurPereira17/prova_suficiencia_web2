import api from "./client";

export async function listarUsuarios() {
  const { data } = await api.get("/usuarios");
  return data;
}

export async function removerUsuario(id) {
  const { data } = await api.delete(`/usuarios/${id}`);
  return data;
}