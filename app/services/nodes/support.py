# app/services/nodes/support.py
from app.services.state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings
from app.core.prompts import SUPPORT_PROMPT

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model=settings.DEFAULT_MODEL, 
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0.3 # Slightly higher temperature for better empathy
)

async def support_node(state: AgentState):
    """Logic: Empathy, Refund policy explanation, and Human Escalation"""
    
    biz = state.get("business_context", {})
    
    # Format the specialized Support Prompt
    prompt = SUPPORT_PROMPT.format(
        business_name=biz.get("business_name", "the store"),
        return_policy=biz.get("return_policy", "our standard policy")
    )

    # Generate the empathetic response using LLM
    # We pass the conversation history so the AI knows WHAT the complaint is
    response = await llm.ainvoke([
        ("system", prompt),
        *state["messages"]
    ])
    
    final_text = response.content

    # --- CRITICAL: Pydantic String Enforcement ---
    if isinstance(final_text, list):
        final_text = "".join(
            [block.get("text", "") if isinstance(block, dict) else str(block) 
             for block in final_text]
        )
    
    # We set escalate to True because complaints/refunds 
    # usually require human oversight in your project requirements
    return {
        "response_message": str(final_text),
        "escalate": True
    }