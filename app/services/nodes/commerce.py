# app/services/nodes/commerce.py
from app.services.state import AgentState
from app.core.prompts import COMMERCE_PROMPT
from langchain_groq import ChatGroq
from app.core.config import settings


llm = ChatGroq(
    model=settings.DEFAULT_MODEL,
    groq_api_key=settings.GROQ_API_KEY,
    temperature=0
)
async def commerce_node(state: AgentState):
    biz = state.get("business_context", {})
    prompt = COMMERCE_PROMPT.format(
        business_name=biz.get("business_name", "Store"),
        tone=biz.get("tone", "friendly"),
        inventory=state.get("inventory", []),
        shipping_policy=biz.get("shipping_policy", ""),
        return_policy=biz.get("return_policy", "")
    )

    response = await llm.ainvoke([("system", prompt)] + state["messages"])
    
    # CRITICAL FIX: Ensure the output is a string
    content = response.content
    if isinstance(content, list):
        # Extract text if it's returned as a list of dicts
        content = "".join([block.get("text", "") if isinstance(block, dict) else str(block) for block in content])
    
    return {"response_message": str(content)}