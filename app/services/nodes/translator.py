# app/services/nodes/translator.py
from app.services.state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

# 1. Initialize the LLM inside this file
llm = ChatGoogleGenerativeAI(
    model=settings.DEFAULT_MODEL, 
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0
)

async def translator_node(state: AgentState):
    target_lang = state.get("language", "english")
    current_text = state.get("response_message", "")

    # 2. Logic to handle Roman Urdu translation
    if target_lang == "roman_urdu" and current_text:
        res = await llm.ainvoke(
            f"Translate the following shop response into natural, friendly Roman Urdu (Latin script): {current_text}"
        )
        final_text = res.content
    else:
        final_text = current_text

    # 3. CRITICAL: Pydantic String Enforcement
    # If Gemini returns a list of dicts, extract the text string
    if isinstance(final_text, list):
        # Join all text parts if it's a list (common in newer LangChain/Gemini versions)
        final_text = "".join(
            [block.get("text", "") if isinstance(block, dict) else str(block) 
             for block in final_text]
        )
    
    # Final safety check: ensure it is a plain string
    return {"response_message": str(final_text)}