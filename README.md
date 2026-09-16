# Function Calling & Tool Integration
## Month 3 Sprint A — Final Project


## Overview

In this sprint, you learned how to give LLMs the ability to act — through function calling, multi-tool routing, and multi-agent handoffs. Your final project brings all of that together into one working agentic system.

Build any project of your choice using the skills from all three tasks. The only requirement is that it must have at least two agents, at least two tools, and a handoff between agents.

---

## Submission Guidelines

### 1. Fork the Repository

Click the **Fork** button at the top-right of this repository.

### 2. Clone Your Fork

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 3. Create a Folder with Your Name

Use lowercase letters and hyphens — no spaces.

```
<repo-name>/
└── john-doe/
    ├── main.py
    ├── agents.py
    ├── tools.py
    ├── requirements.txt
    ├── .env.example
    ├── .gitignore
    └── README.md
```

> ⚠️ Place all your files inside your named folder. Do not put them in the root of the repo.

---

## File Responsibilities

| File | Purpose |
|---|---|
| `main.py` | Entry point — runs the agent system, handles user input, calls `handle_query()` |
| `agents.py` | All agent functions — generalist, specialists, intent classifier, handoff logic |
| `tools.py` | All tool functions — mock databases, tool implementations, tool schemas |
| `requirements.txt` | All dependencies needed to run the project |
| `.env.example` | Shows what environment variables are needed (without actual values) |
| `.gitignore` | Ensures `.env` and cache files are not committed |
| `README.md` | Your own project README inside your folder (see template below) |

> You are free to add more files if your project needs them (e.g. `database.py` for mock data, `config.py` for constants). The structure above is the minimum expected.

---

## Your README.md Template

Include a `README.md` inside your named folder describing your project:

```markdown
## Project Name

## What it does
A short description of your agentic system and the problem it solves.

## Agents
- **Agent 1 (Generalist):** What it handles
- **Agent 2 (Specialist):** What it handles and what tools it uses
- *(add more if applicable)*

## Tools
- `tool_name(params)` — what it does
- `tool_name(params)` — what it does

## Tech Stack
- Language: Python
- LLM: Groq (`model name`)
- Function Calling: Groq Tool Use API

## How to Run

### 1. Clone and navigate to your folder
git clone ...
cd john-doe

### 2. Install dependencies
pip install -r requirements.txt

### 3. Set up environment variables
cp .env.example .env
# Add your GROQ_API_KEY to .env

### 4. Run
python main.py

## Sample Interaction
User: <example query>
→ Handled by: <agent name>

User: <example query that triggers handoff>
→ Handoff triggered → <specialist agent>
→ Tool called: <tool name>
→ Response: ...

## Environment Variables
| Variable | Description |
|---|---|
| GROQ_API_KEY | Your Groq API key from console.groq.com |
```

---

## .env.example

Your `.env.example` should look like this:

```
GROQ_API_KEY=your_groq_api_key_here
```

---

## .gitignore

Your `.gitignore` should include at minimum:

```
.env
__pycache__/
*.pyc
*.pyo
.DS_Store
```

---

## requirements.txt

Generate this after setting up your environment:

```bash
pip freeze > requirements.txt
```

At minimum it should include:

```
groq
python-dotenv
```

---

## Commit and Push

```bash
git add .
git commit -m "Add submission - John Doe"
git push origin main
```

---

## Open a Pull Request

1. Go to your fork on GitHub
2. Click **Contribute → Open Pull Request**
3. Set the PR title to: `Submission - John Doe`
4. Submit the pull request

> 📌 Your submission is complete once the PR is opened.

---

## What to Submit

| File | Required |
|---|---|
| `main.py` | ✅ Yes |
| `agents.py` | ✅ Yes |
| `tools.py` | ✅ Yes |
| `requirements.txt` | ✅ Yes |
| `.gitignore` | ✅ Yes |
| `.env.example` | ✅ Yes |
| `README.md` inside your folder | ✅ Yes |
| `.env` | ❌ Never commit this |

---

## Minimum Project Requirements

- At least **2 agents** (one generalist, at least one specialist)
- At least **2 tools** accessible to the specialist agent
- A working **handoff** from generalist to specialist with context passed
- Handoff must be **logged** — print which agent triggered it, why, and what was passed
- Only **one handoff per query** — no ping-ponging
- Specialist must **not be reachable directly** by the user

---
