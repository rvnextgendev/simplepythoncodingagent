from langchain_core.messages import HumanMessage
from src.agent import build_graph

# System prompt instructs the agent to verify code via the run_python_code tool
# before returning the final answer to the user.
SYSTEM_PROMPT = (
    "You are an expert Python coding assistant. "
    "When asked to write or fix code, produce clean, working Python. "
    "Use the run_python_code tool to verify your code actually runs correctly "
    "before presenting the final answer."
)


def run(task: str):
    """Run the coding agent on a given task string and print the result."""
    graph = build_graph()

    # Seed the conversation with the system prompt and the user task
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        HumanMessage(content=task),
    ]

    result = graph.invoke({"messages": messages})

    # The last message in the list is always the final AI response
    final = result["messages"][-1]
    print("\n=== Coding Agent Result ===")
    print(final.content)


if __name__ == "__main__":
    import sys

    # Accept the task as a CLI argument; fall back to a default demo task
    task = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else "Write a Python function that returns the nth Fibonacci number using recursion with memoization."
    )
    run(task)
