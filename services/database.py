from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.model.chat_history import ChatHistory


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.engine = create_engine(
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
            echo=True,
        )

    def get(self, chatid):
        """
        Get chat history from database.

        Args:
            chatid (int): The chat id.

        Returns:
            list: The chat history, as a list of dicts.
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()

        chat_history = session.query(ChatHistory).filter_by(chatid=chatid).first()

        if chat_history:
            return chat_history.history
        return None

    def set(self, chatid, history):
        """
        Set chat history in database.

        Args:
            chatid (int): The chat id.
            history (list): The chat history, as a list of dicts.
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()

        existing_chat_history = (
            session.query(ChatHistory).filter_by(chatid=chatid).first()
        )

        if existing_chat_history:
            existing_chat_history.history = history
        else:
            chat_history = ChatHistory(chatid=chatid, history=history)
            session.add(chat_history)
        session.commit()
