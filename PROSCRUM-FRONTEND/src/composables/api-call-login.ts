import { setToken } from "./token-administration.ts";
import type { LoginData } from "../types/types.ts";
import { useErrorController } from "@/composables/error-controller.ts";
import { i18n } from "@/main.ts";
import type { Composer } from "vue-i18n";




const { setError } = useErrorController();

export async function apiCallLogin(loginData: LoginData): Promise<void> {

  const formData = new URLSearchParams();
  formData.append("username", loginData.username);
  formData.append("password", loginData.password);
  formData.append("grant_type", "password");

  try {
    const rawResponse = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData.toString(),
    });

    if (!rawResponse.ok) {
      throw new Error(`HTTP-Fehler! Status: ${rawResponse.status}`);
    }

    const responseData = await rawResponse.json();
    console.log("2: Token erhalten:", responseData);
    setToken(responseData.access_token);

  } catch (error) {
    const globalT = (i18n.global as Composer).t; //<---
    setError(globalT('error.login.user_not_found')); //<---
  }
}
