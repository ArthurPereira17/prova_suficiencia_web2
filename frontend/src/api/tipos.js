import api from "./client";

export async function listarTipos() {
  const { data } = await api.get("/tipos");
  return data;
}

export async function criarTipo(payload) {
  const { data } = await api.post("/tipos", payload);
  return data;
}