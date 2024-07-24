import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types.content import Content, Part
import os
import pprint


class GeminiClient:
    # _instances = None

    # def __new__(cls, model_name=None):
    #     print("##################################################", model_name)
    #     if cls._instance is None:
    #         cls._instance = super().__new__(cls)
    #     return cls._instance

    def __init__(self, model_name=None):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model_name = (
            model_name or os.getenv("GEMINI_MODEL") or "gemini-1.5-flash-latest"
        )
        print(f"Using Gemini model: {self.model_name}")
        genai.configure(api_key=self.api_key)
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]

        self.model = genai.GenerativeModel(
            self.model_name,
        )

    def list_models(self):
        for model in genai.list_models():
            pprint.pprint(model)

    def get_response(self, prompt: str):
        """
        Get standalone response from model. Does not store conversation history.

        Args:
            prompt (str): The text prompt.

        Returns:
            text: the output, as str, of the model.
        """
        try:
            response = self.model.generate_content(
                prompt,
                stream=False,
                safety_settings=self.safety_settings,
            )
        except Exception as e:
            raise e

        return response.text

    def load_history_from_dict(self, history_data):
        return [
            Content(parts=[Part(text=message["content"])], role=message["role"])
            for message in history_data
        ]

    def history_to_dict(self, history):
        return [
            {"role": message.role, "content": message.parts[0].text}
            for message in history
        ]

    def chat(self, prompt, history_data=None):
        """
        Get a chat response from model. Stores conversation history.

        Args:
            prompt (str): The message prompt.
            history_data (list): List of dicts representing chat history.
                                  Ex: [{"role": "user", "content": "Olá"},
                                       {"role": "model", "content": "Oi!"}]

        Returns:
            text: the current prompt output, as str, of the model.
        """
        history = []
        if history_data:
            history = self.load_history_from_dict(history_data)

        try:
            chat_instance = self.model.start_chat(history=history)
            response = chat_instance.send_message(
                prompt, safety_settings=self.safety_settings
            )

            return response.text, self.history_to_dict(chat_instance.history)
        except Exception as e:
            raise e
