import api from "./client";

export async function listarEquipamentos() {
  const { data } = await api.get("/equipamentos");
  return data.equipamentos;
}

export async function buscarEquipamento(id) {
  const { data } = await api.get(`/equipamentos/${id}`);
  return data;
}

export async function criarEquipamento(payload) {
  const { data } = await api.post("/equipamentos", payload);
  return data;
}

export async function atualizarEquipamento(id, payload) {
  const { data } = await api.put(`/equipamentos/${id}`, payload);
  return data;
}

export async function removerEquipamento(id) {
  const { data } = await api.delete(`/equipamentos/${id}`);
  return data;
}