import axios from "axios";

const BASE_URL = "http://localhost:8080/RestAPIFurb";

// Login usa form-urlencoded (padrão OAuth2 exigido pelo FastAPI/OAuth2PasswordRequestForm)
export async function login(username, password) {
  const params = new URLSearchParams();
  params.append("username", username);
  params.append("password", password);

  const { data } = await axios.post(`${BASE_URL}/auth/login`, params, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return data.access_token;
}