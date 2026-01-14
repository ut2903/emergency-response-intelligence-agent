from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from state import State
from prompt import system_prompt
from analytics import summarize_conversation
from config import OPENAI_API_KEY


# =========================
# LLM INITIALIZATION
# =========================

# Primary real-time call handling model
llm_call = ChatOpenAI(
    model="gpt-4o-mini",          # Fast, low-latency model for live calls
    temperature=0.2,
    max_tokens=90,
    api_key=OPENAI_API_KEY,
)

# Post-call summarization model
llm_summary = ChatOpenAI(
    model="gpt-4o-mini",          # Can be swapped with larger model if needed
    temperature=0.1,
    max_tokens=512,
    api_key=OPENAI_API_KEY,
)

# NOTE:
# For Indic / multilingual deployments, this LLM can be replaced with:
# - Sarvam models
# - Azure-hosted regional LLMs
# - Any server-hosted chat model
# without changing the graph logic.


# =========================
# GRAPH NODES
# =========================

def llm_call_node(state: State) -> State:
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(state["conversation"])

    response = llm_call.invoke(messages)

    state["conversation"].append({
        "role": "assistant",
        "content": response.content
    })

    # Call termination detection (your original logic)
    if '"call_status": "END"' in response.content:
        state["call_status"] = "END"
    else:
        state["call_status"] = "ONGOING"

    return state


def summarize_conversation_node(state: State) -> State:
    # Uses your EXACT summarization prompt inside analytics.py
    summary = summarize_conversation(state, llm_summary)
    state["summary"] = summary
    return state


# =========================
# LANGGRAPH WORKFLOW
# =========================

workflow = StateGraph(State)

# Start node
workflow.add_node("llm_call", llm_call_node)

# Post-call node
workflow.add_node("summarize_conversation", summarize_conversation_node)

# Entry point
workflow.set_entry_point("llm_call")

# SIMPLE, EXPLICIT CONTROL FLOW
workflow.add_conditional_edges(
    "llm_call",
    lambda state: state["call_status"],
    {
        "ONGOING": END,
        "END": "summarize_conversation",
    }
)

workflow.add_edge("summarize_conversation", END)

graph = workflow.compile()
