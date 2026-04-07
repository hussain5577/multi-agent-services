# app/services/state.py
from typing import Annotated, TypedDict, List, Optional, Dict, Any
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
class AgentState(TypedDict):
    messages: Annotated[List, add_messages]
    conversation_id: str
    channel: str
    customer: Dict[str, Any]
    business_context: Dict[str, Any]
    inventory: List[Dict[str, Any]]
 
    intent: str
    confidence: float
    language: str
    response_message: str
    backend_action: Optional[Dict[str, Any]]
    escalate: bool