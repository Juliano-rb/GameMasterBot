import google.generativeai as genai
import os
import pprint


class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model = os.getenv("GEMINI_MODEL") or "gemini-1.5-flash-latest"
        print(f"Using Gemini model: {self.model}")
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
            "gemini-1.5-flash-latest",
        )
        self.chat_instance = None

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

    def chat(self, prompt):
        """
        Get a chat response from model. Stores conversation history.

        Args:
            prompt (str): The message prompt.

        Returns:
            text: the current prompt output, as str, of the model.
        """
        try:
            if not self.chat_instance:
                self.chat_instance = self.model.start_chat(history=[])
            response = self.chat_instance.send_message(
                prompt, safety_settings=self.safety_settings
            )
            return response.text
        except Exception as e:
            raise e
