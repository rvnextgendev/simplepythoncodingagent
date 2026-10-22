import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from src.agent import build_graph

st.set_page_config(page_title="Coding Agent", page_icon="🤖", layout="wide")
st.title("🤖 Coding Agent")
st.caption("Powered by Groq + Qwen via LangGraph")

SYSTEM_PROMPT = (
    "You are an expert Python coding assistant. "
    "When asked to write or fix code, produce clean, working Python. "
    "Use the run_python_code tool to verify your code actually runs correctly "
    "before presenting the final answer."
)

# Cache the graph so it's not rebuilt on every interaction
@st.cache_resource
def get_graph():
    return build_graph()


# Initialise chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render existing chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if task := st.chat_input("Ask the agent to write or fix Python code..."):

    # Show and store user message
    st.session_state.messages.append({"role": "user", "content": task})
    with st.chat_message("user"):
        st.markdown(task)

    # Run agent
    with st.chat_message("assistant"):
        with st.spinner("Agent is thinking..."):
            graph = get_graph()
            result = graph.invoke({
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    HumanMessage(content=task),
                ]
            })

        # Show tool calls in an expander so they don't clutter the main view
        tool_steps = [
            m for m in result["messages"]
            if isinstance(m, ToolMessage)
        ]
        if tool_steps:
            with st.expander(f"🔧 Tool executions ({len(tool_steps)})"):
                for t in tool_steps:
                    st.code(t.content, language="text")

        # Final AI answer is the last message
        final = result["messages"][-1]
        answer = final.content if hasattr(final, "content") else str(final)
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
