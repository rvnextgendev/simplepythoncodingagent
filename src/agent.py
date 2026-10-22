import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from src.tools import run_python_code

# Load GROQ_API_KEY and LLM_MODEL from .env
load_dotenv()


# ---------- State ----------
# add_messages reducer appends new messages instead of overwriting,
# keeping the full conversation history across agent/tool turns.
class State(TypedDict):
    messages: Annotated[list, add_messages]


# ---------- LLM ----------

def build_llm() -> ChatGroq:
    """Instantiate the Groq chat model from environment config."""
    return ChatGroq(
        api_key=os.environ["GROQ_API_KEY"],
        model=os.environ.get("LLM_MODEL", "qwen/qwen3.8-27b"),
    )


# Tools available to the agent
TOOLS = [run_python_code]


def build_graph() -> StateGraph:
    """
    Build and compile the LangGraph agent graph.

    Graph flow:
        [agent] → (has tool calls?) → [tools] → [agent] → ... → END
    The agent node calls the LLM; if it requests a tool, the tools node
    executes it and sends the result back to the agent node.
    """
    # Bind tools so the LLM knows it can call run_python_code
    llm = build_llm().bind_tools(TOOLS)

    def call_model(state: State):
        """Invoke the LLM with the current message history."""
        response = llm.invoke(state["messages"])
        return {"messages": [response]}

    # ToolNode automatically routes tool call requests to the right function
    tool_node = ToolNode(TOOLS)

    graph = StateGraph(State)

    # Register nodes
    graph.add_node("agent", call_model)
    graph.add_node("tools", tool_node)

    # Entry point: always start at the agent node
    graph.set_entry_point("agent")

    # After agent: go to tools if there are tool calls, otherwise END
    graph.add_conditional_edges("agent", tools_condition)

    # After tools: always return to agent for the next LLM response
    graph.add_edge("tools", "agent")

    return graph.compile()
