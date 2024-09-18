from sqlalchemy import Column, Integer, TIMESTAMP, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

Base = declarative_base()
engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=True,
)


class ChatHistory(Base):
    __tablename__ = "chat_history"

    chatid = Column(Integer, primary_key=True, nullable=False, unique=True)
    history = Column(JSON, nullable=True, default="{}'::jsonb")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp()
    )

    def __repr__(self):
        return f"ChatHistory {self.name}"


Base.metadata.create_all(engine)
