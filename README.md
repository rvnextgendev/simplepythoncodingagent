# Coding Agent

A LangGraph-based coding agent powered by Groq + Qwen. It writes Python code, runs it to verify it works, and self-corrects on errors before returning the final answer.

## How it works

```
User Task → Agent (LLM) → run_python_code tool → Agent → ... → Final Answer
```

If the generated code has errors, the agent sees the stderr output and fixes it automatically until the code runs clean.

## Setup

**1. Create and activate a virtual environment**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**2. Install dependencies**
```powershell
pip install -r requirements.txt
```

**3. Configure your API key in `.env`**
```
GROQ_API_KEY=your_key_here
LLM_PROVIDER=groq
LLM_MODEL=qwen/qwen3.8-27b
```

## Usage

```powershell
python main.py "Write a Python function to check if a string is a palindrome"
```

```powershell
python main.py "Fix this broken Python code: print('hello'"
```

```powershell
python main.py "Write a binary search function with tests"
```

Running without arguments uses a built-in Fibonacci demo task.

## Project structure

```
codingAgent/
├── .env                 # API keys (not committed)
├── requirements.txt     # Pinned dependencies
├── main.py              # CLI entry point
└── src/
    ├── agent.py         # LangGraph graph definition
    └── tools.py         # run_python_code tool
```

## Dependencies

| Package | Purpose |
|---|---|
| `langgraph` | Agent loop / state graph |
| `langchain-groq` | Groq LLM integration |
| `langchain-core` | LangChain base abstractions |
| `python-dotenv` | Load `.env` config |
