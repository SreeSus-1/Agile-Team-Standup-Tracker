import requests

class BaseAgent:
    def __init__(self, model="phi3"):
        self.model = model

    def call_ollama(self, prompt: str) -> str:
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=600
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()

        except requests.exceptions.Timeout:
            return "ERROR: Ollama request timed out."

        except requests.exceptions.ConnectionError:
            return "ERROR: Could not connect to Ollama. Make sure Ollama is running."

        except Exception as e:
            return f"ERROR: {str(e)}"