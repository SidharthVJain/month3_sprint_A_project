## General-Purpose Agentic Assistant

## What it does
A simple agentic assistant that accepts one user query, classifies it through a Generalist Agent, and either answers directly or hands the query to one specialist. General queries are answered by the Generalist. Math-heavy queries go to the Calculation Specialist, which can use a calculator and unit converter. Factual queries go to the Research Specialist, which can use web search.

The handoff includes the original query and classification context and is printed to the terminal. Each query can trigger at most one handoff.

## Agents
- **Agent 1 (Generalist):** Classifies every user query and directly answers normal general-purpose requests.
- **Agent 2 (Calculation Specialist):** Handles math-heavy queries and uses the calculator and unit converter tools.
- **Agent 3 (Research Specialist):** Handles factual queries and uses the web search tool.
- Specialists are internal functions and are only reached through the Generalist handoff.

## Tools
- `calculate(expression)`: safely evaluates common mathematical expressions.
- `unit_converter(value, from_unit, to_unit)`: converts length, mass, time, and temperature units.
- `web_search(query, max_results)`: searches the web with DuckDuckGo (`ddgs`) and returns titles, URLs, and snippets.

## Tech Stack
- Language: Python
- LLM: Groq (`openai/gpt-oss-120b`)
- Function Calling: Groq Tool Use API

## How to Run

### 1. Clone and navigate to your folder
git clone https://github.com/SidharthVJain/month3_sprint_A_project.git
cd month3_sprint_A_project

### 2. Install dependencies
pip install -r requirements.txt

### 3. Set up environment variables
cp .env.example .env
# Add your GROQ_API_KEY to .env

### 4. Run
python main.py

## Sample Interaction
General-Purpose Assistant
Type 'exit' to quit.

You: How much is 100 degrees Fahrenheit in Celsius
[Handoff] Generalist Agent -> Calculation Specialist
[Handoff reason] User requests a temperature conversion calculation
[Handoff context] {"original_query": "How much is 100 degrees Fahrenheit in Celsius", "classified_intent": "math", "reason": "User requests a temperature conversion calculation", "handoff_number": 1}
[Tool] unit_converter({'from_unit': 'F', 'to_unit': 'C', 'value': 100})
[Tool result] {'result': 37.77777777777778, 'unit': 'C'}

Assistant: 100 °F is approximately **37.78 °C**.


You: What is the age of Narendra Modi
[Handoff] Generalist Agent -> Research Specialist
[Handoff reason] User asks for current factual information about a real person's age
[Handoff context] {"original_query": "What is the age of Narendra Modi", "classified_intent": "research", "reason": "User asks for current factual information about a real person's age", "handoff_number": 1}
[Tool] web_search({'max_results': 5, 'query': 'Narendra Modi age 2026'})
[Tool result] {'query': 'Narendra Modi age 2026', 'results': [{'title': 'Narendra Modi - WikipediaPrime minister narendra modi birthday 2026 know 76 years of ..
...

Assistant: Narendra Modi was born on 17 September 1950. As of today (21 September 2026) he is **76 years old** (he turned 76 on 17 September 2026)【https://en.wikipedia.org/wiki/Narendra_Modi】.

## Environment Variables
| Variable | Description |
|---|---|
| GROQ_API_KEY | Your Groq API key from console.groq.com |
