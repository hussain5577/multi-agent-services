# app/services/nodes/translator.py

from app.services.state import AgentState
from langchain_groq import ChatGroq
from app.core.config import settings


# Initialize once
llm = ChatGroq(
    model=settings.DEFAULT_MODEL,
    groq_api_key=settings.GROQ_API_KEY,
    temperature=0
)


async def translator_node(state: AgentState):

    # If safety already generated response → use it
    response_text = state.get("response_message", "")

    if not response_text:
        # Fallback default message
        response_text = (
            "Shukriya aap ke message ka. "
            "Hum jald aap ki madad karte hain."
        )

    target_lang = state.get("language", "english")

    # Only translate if Roman Urdu required
    if target_lang == "roman_urdu":

        prompt = f"""
Translate the following shop response into natural,
friendly Roman Urdu (Latin script).
- Use Pakistani Roman Urdu style
- Do NOT use Hindi words like:
  Dhanyavad
  Kripya
  Aapka
  Kripaya
- Use Pakistani words like:
  Shukriya
  Barah-e-karam
  Aap
  Meherbani
Text:
{response_text}

Rules:
- Keep tone friendly
- Keep meaning same
- Use simple Roman Urdu
"""

        try:
            res = await llm.ainvoke(prompt)
            response_text = res.content.strip()

        except Exception as e:
            print(f"Translator Error: {e}")
            # fallback → use original English text

    # Always return clean string
    return {
        **state,
        "response_message": str(response_text)
    }