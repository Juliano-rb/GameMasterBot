from supabase import create_client, Client
from config import SUPABASE_KEY, SUPABASE_URL


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def get(self, chatid):
        """
        Get chat history from database.

        Args:
            chatid (int): The chat id.

        Returns:
            list: The chat history, as a list of dicts.
        """
        response = (
            self.supabase.table("chat_history")
            .select("*")
            .eq("chatid", chatid)
            .execute()
        )

        if response.data:
            return response.data[0]["history"]
        return None

    def set(self, chatid, history):
        """
        Set chat history in database.

        Args:
            chatid (int): The chat id.
            history (list): The chat history, as a list of dicts.
        """

        self.supabase.table("chat_history").upsert(
            {"chatid": chatid, "history": history},
        ).execute()
