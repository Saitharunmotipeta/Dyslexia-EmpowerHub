import api from "@/lib/api/axios";
import { LoginPayload, RegisterPayload, AuthResponse } from "./types";

export const loginUser = async (
  payload: LoginPayload
): Promise<AuthResponse> => {
  const params = new URLSearchParams();
  params.append("username", payload.username); // FastAPI expects username
  params.append("password", payload.password);

  const { data } = await api.post("/auth/login", params, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  return data;
};

export const registerUser = async (
  payload: RegisterPayload
): Promise<AuthResponse> => {
  const { data } = await api.post("/auth/register", payload);
  return data;
};
