from langgraph.graph import MessagesState
from typing import Optional

class AppState(MessagesState):
    workflow: Optional[str]
    user_id: str