import { ref } from "vue";

// Globale Fehler-Variable
const errorText = ref<string>("");

// Funktionen zum Setzen/Löschen des Fehlers
export function useErrorController() {
  const setError = (err: string) => {
    errorText.value = err;
  };

  const clearError = () => {
    errorText.value = "";
  };

  return { errorText, setError, clearError };
}

// **Globale Instanz von errorText exportieren**
export { errorText };
