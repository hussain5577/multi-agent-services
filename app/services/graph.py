# app/services/graph.py
from langgraph.graph import StateGraph, END
from app.services.state import AgentState
from app.services.nodes.classifier import classifier_node
from app.services.nodes.commerce import commerce_node
from app.services.nodes.support import support_node
from app.services.nodes.translator import translator_node

workflow = StateGraph(AgentState)

workflow.add_node("classifier", classifier_node)
workflow.add_node("commerce", commerce_node)
workflow.add_node("support", support_node)
workflow.add_node("translator", translator_node)

workflow.set_entry_point("classifier")

def route_intent(state: AgentState):
    # Default to unknown if intent is missing
    intent = state.get("intent", "unknown")
    
    # Log for debugging
    print(f"DEBUG: Routing Intent -> {intent}")
    
    if intent in ["create_order", "product_inquiry", "collect_address", "collect_variant", "collect_quantity"]:
        return "commerce"
    if intent in ["complaint", "refund_request"]:
        return "support"
    
    # If it's a greeting or unknown, go straight to translator/general response
    return "translator"

workflow.add_conditional_edges("classifier", route_intent)
workflow.add_edge("commerce", "translator")
workflow.add_edge("support", "translator")
workflow.add_edge("translator", END)

app_graph = workflow.compile()