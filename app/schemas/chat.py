# app/schemas/chat.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal

# --- INPUT SCHEMAS ---

class Customer(BaseModel):
    name: str
    username: str
    language: str = "auto"

class BusinessContext(BaseModel):
    business_name: str
    tone: str
    shipping_policy: str
    return_policy: str
    payment_methods: List[str]

class InventoryItem(BaseModel):
    product_id: str
    name: str
    price: int
    variants: List[str]
    stock: Dict[str, int]

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    message: str

class ChatPayload(BaseModel):
    conversation_id: str
    channel: Literal["instagram_dm", "instagram_comment"]
    customer: Customer
    business_context: BusinessContext
    inventory: List[InventoryItem]
    conversation_history: List[ChatMessage]

# --- OUTPUT SCHEMAS ---

class BackendAction(BaseModel):
    type: str
    product_id: Optional[str] = None
    variant: Optional[str] = None
    quantity: Optional[int] = None

class ChatResponse(BaseModel):
    intent: str
    confidence: float
    response_message: str
    backend_action: Optional[BackendAction] = None
    escalate: bool = False

# --- LLM STRUCTURED OUTPUT ---

class IntentResponse(BaseModel):
    intent: Literal[
        "product_inquiry",
        "create_order",
        "collect_variant", 
        "collect_quantity",
        "collect_address",
        "collect_phone", 
        "order_status",
        "faq", 
        "complaint", 
        "refund_request", 
        "greeting",
        "unknown",
        "abusive",        
        "off_topic",     
        "human_escalation"
    ]
    language: Literal[
        "english", 
        "urdu", 
        "roman_urdu"
        ]
    confidence: float



