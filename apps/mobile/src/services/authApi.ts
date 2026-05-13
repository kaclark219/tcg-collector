import { apiRequest } from "@/services/apiClient";
import { LoginResponse } from "@/types";

export async function loginProfile(username: string, pin: string) {
  return apiRequest<LoginResponse>("/profiles/login", {
    method: "POST",
    body: { username, pin },
  });
}

