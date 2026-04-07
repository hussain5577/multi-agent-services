from app.services.state import AgentState

async def safety_guard_node(state: AgentState):

    intent = state.get("intent", "unknown")

    print(f"DEBUG: Safety Check -> {intent}")

    if intent == "abusive":
        return {
            "response": (
                "Barah-e-karam ghalat alfaaz istemal na karein. "
                "Agar koi masla hai to bata dein, hum madad karne ki koshish karenge."
            ),
            "route": "translator"
        }

    if intent == "off_topic":
        return {
            "response": (
                "Main sirf products aur orders se related madad kar sakta hoon. "
                "Aap product ya order ka sawal pooch sakte hain."
            ),
            "route": "translator"
        }

    return {"route": "continue"}