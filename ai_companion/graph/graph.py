from langgraph.graph import StateGraph, START, END
from ai_companion.graph.state import AppState
from ai_companion.graph.nodes import (
conversation_node,
router_node,
image_node,
audio_node,
tool_node
)

def route_decision(state: AppState):
    workflow = state.get("workflow")

    if workflow not in ["conversation", "image", "audio"]:
        print("⚠️ Invalid workflow:", workflow)
        return "conversation"  # fallback

    return workflow

def create_graph():
    builder = StateGraph(AppState)

    # Add nodes
    builder.add_node("router", router_node)
    builder.add_node("conversation", conversation_node)
    builder.add_node("image", image_node)
    builder.add_node("audio", audio_node)
    builder.add_node("tool", tool_node)

    #Entry 
    builder.add_edge(START, "router")
    
    #Conditional routing 
    builder.add_conditional_edges(
        "router",
        route_decision,
        {
            "conversation": "conversation",
            "image" : "image", 
            "audio" : "audio",
            "tool" : "tool"
        },
    )
    
    #End all branches 
    builder.add_edge("conversation", END)
    builder.add_edge("image", END)
    builder.add_edge("audio", END)
    builder.add_edge("tool", END)

    return builder.compile()