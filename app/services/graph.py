# app/services/graph.py

from langgraph.graph import StateGraph, END

from app.services.state import AgentState

from app.services.nodes.classifier import classifier_node
from app.services.nodes.commerce import commerce_node
from app.services.nodes.support import support_node
from app.services.nodes.translator import translator_node
from app.services.nodes.safety import safety_guard_node


# Create workflow
workflow = StateGraph(AgentState)


# -----------------------------
# Add Nodes
# -----------------------------

workflow.add_node("classifier", classifier_node)

workflow.add_node("safety", safety_guard_node)  # NEW

workflow.add_node("commerce", commerce_node)

workflow.add_node("support", support_node)

workflow.add_node("translator", translator_node)


# -----------------------------
# Entry Point
# -----------------------------

workflow.set_entry_point("classifier")


# -----------------------------
# Safety Routing
# -----------------------------

def route_after_safety(state: AgentState):

    intent = state.get("intent", "unknown")

    print(f"DEBUG: After Safety Intent -> {intent}")

    # 🚨 Abuse Handling
    if intent == "abusive":
        return "translator"

    # 🚫 Off-topic Handling
    if intent == "off_topic":
        return "translator"

    # 🛒 Commerce Flow
    if intent in [
        "create_order",
        "product_inquiry",
        "collect_address",
        "collect_variant",
        "collect_quantity"
    ]:
        return "commerce"

    # 🧾 Support Flow
    if intent in [
        "complaint",
        "refund_request"
    ]:
        return "support"

    # 👋 Greeting / FAQ / Unknown
    return "translator"


# -----------------------------
# Edges
# -----------------------------

# classifier → safety
workflow.add_edge("classifier", "safety")


# safety → dynamic routing
workflow.add_conditional_edges(
    "safety",
    route_after_safety
)


# commerce → translator
workflow.add_edge("commerce", "translator")


# support → translator
workflow.add_edge("support", "translator")


# translator → END
workflow.add_edge("translator", END)


# -----------------------------
# Compile Graph
# -----------------------------

app_graph = workflow.compile()