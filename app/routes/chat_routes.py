# app/routes/chat_routes.py
from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatPayload, ChatResponse
from app.services.graph import app_graph

router = APIRouter()
@router.post("/process-chat", response_model=ChatResponse)
async def process_chat(payload: ChatPayload):
    # Mapping the incoming JSON directly to the Graph State
    # Every key in AgentState MUST be initialized here
    initial_state = {
        # Core History
        "messages": [("user", m.message) for m in payload.conversation_history],
        
        # Section 16 Isolation Data (From Payload)
        "business_context": payload.business_context.model_dump(), 
        "inventory": [item.model_dump() for item in payload.inventory],
        
        # Classification Defaults (Required to avoid KeyErrors)
        "intent": "unknown",
        "confidence": 0.0,
        "language": "english",
        
        # Commerce & Output Defaults (Required)
        "order_draft": None,
        "response_message": "",
        "backend_action": None,
        "escalate": False
    }

    try:
        # Execute the Graph
        result = await app_graph.ainvoke(initial_state)
        
        return ChatResponse(
            intent=result.get("intent", "unknown"),
            confidence=result.get("confidence", 0.0),
            response_message=result.get("response_message", ""),
            backend_action=result.get("backend_action"),
            escalate=result.get("escalate", False)
        )
    except Exception as e:
        print(f"❌ Graph Error: {str(e)}")
        # This catch-all returns the escalation response you saw earlier
        return ChatResponse(
            intent="human_escalation",
            confidence=0.0,
            response_message="System technical difficulty. Connecting you to a human.",
            escalate=True
        )