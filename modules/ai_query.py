import requests
import asyncio

class AIQueryHandler:
    def __init__(self, speech_handler, api_key):
        self.speech_handler = speech_handler
        self.api_key = api_key

    async def process_ai_query(self, query):
        try:
            formatted_query = f"Q: {query}\nA: Give a brief, factual answer in one sentence:"
            api_url = "https://api-inference.huggingface.co/models/google/flan-t5-base"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {
                "inputs": formatted_query,
                "parameters": {"max_length": 50, "temperature": 0.7}
            }

            response = await asyncio.to_thread(requests.post, api_url, headers=headers, json=payload)
            if response.status_code == 200:
                answer = response.json()[0]["generated_text"].strip()
                self.speech_handler.speak(answer)
            else:
                self.speech_handler.speak("Sorry, I couldn't process your request")

        except Exception as e:
            print(f"AI query error: {e}")
            self.speech_handler.speak("Sorry, an error occurred")