# app/services/nodes/classifier.py
from app.schemas.chat import IntentResponse
from app.services.state import AgentState  
from langchain_groq import ChatGroq
from app.core.config import settings
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatGroq(
    model=settings.DEFAULT_MODEL,
    groq_api_key=settings.GROQ_API_KEY,
    temperature=0
)

async def classifier_node(state: AgentState):
    # Use a standard prompt instead of structured_output if you keep hitting errors
    # to see if the LLM is actually reaching Google's servers
    structured_llm = llm.with_structured_output(IntentResponse)
    
    # RELIABLE CONTENT EXTRACTION
    messages = state.get('messages', [])
    if not messages:
        return {"intent": "unknown", "language": "english", "confidence": 0.0}

    last_msg = messages[-1]
    
    # LangGraph messages can be tuples or BaseMessage objects
    if isinstance(last_msg, tuple):
        user_content = last_msg[1]
    elif hasattr(last_msg, 'content'):
        user_content = last_msg.content
    else:
        user_content = str(last_msg)

    try:
        result = await structured_llm.ainvoke([
            SystemMessage(content="Classify the user intent for an e-commerce bot. Intents: [product_inquiry, create_order, faq, greeting, unknown]"),
            HumanMessage(content=user_content)
        ])
        
        return {
            "intent": result.intent, 
            "language": result.language,
            "confidence": result.confidence
        }
    except Exception as e:
        # LOG THE ACTUAL ERROR TO CONSOLE
        print(f"!!! Classifier LLM Error: {type(e).__name__} - {e}")
        raise e