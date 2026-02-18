import { setAccessToken } from "@/lib/auth/token-storage";
import { loginUser, registerUser } from "./api";
import { LoginPayload, RegisterPayload } from "./types";

export const authenticateUser = async (payload: LoginPayload) => {
  const response = await loginUser(payload);
  setAccessToken(response.access_token);
  return response;
};

export const createUserAccount = async (payload: RegisterPayload) => {
  const response = await registerUser(payload);
  setAccessToken(response.access_token);
  return response;
};
