import json
import os

from dotenv import load_dotenv
from groq import Groq

from tools import (
    CALCULATION_TOOLS,
    RESEARCH_TOOLS,
    TOOL_FUNCTIONS,
)

load_dotenv()

MODEL = "openai/gpt-oss-120b"
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def classify_intent(query):
    messages = [
        {
            "role": "system",
            "content": """Classify the user's request into exactly one category.

Categories:
- general: normal conversation, explanations, writing, coding help, or other tasks
  that do not need external factual research or heavy calculation.
- math: calculations, equations, arithmetic, percentages, numerical comparisons,
  or unit conversions.
- research: factual questions that benefit from web search, especially current
  information, recent events, specific facts, or information about real entities.

Return only a JSON object in this format:
{"intent": "general|math|research", "reason": "one short reason"}""",
        },
        {"role": "user", "content": query},
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0,
        include_reasoning=False,
    )

    result = json.loads(response.choices[0].message.content)

    if result.get("intent") not in {"general", "math", "research"}:
        return "general", "The classifier returned an invalid category."

    return result["intent"], result.get(
        "reason",
        "Specialist handling is useful."
    )


def generalist_answer(query):
    messages = [
        {
            "role": "system",
            "content": """You are the Generalist Agent.

Answer the user's request directly and clearly.

Do not pretend to have live web access or calculator tools.
The user has already been classified as a general request.""",
        },
        {"role": "user", "content": query},
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.4,
        include_reasoning=False,
    )

    return response.choices[0].message.content


def run_tool_agent(query, context, system_prompt, tools):
    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": f"""Original user query:
{query}

Handoff context:
{context}

Do the task using the available tools when needed.
Return a clear final answer for the user.""",
        },
    ]

    for _ in range(4):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.2,
            include_reasoning=False,
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content

        # Add only the fields required by the next API request.
        # This avoids sending unsupported fields such as "annotations".
        messages.append(
            {
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                    for tool_call in message.tool_calls
                ],
            }
        )

        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            function = TOOL_FUNCTIONS.get(function_name)

            if function is None:
                result = {
                    "error": f"Unknown tool: {function_name}"
                }
            else:
                try:
                    result = function(**function_args)
                except Exception as error:
                    result = {"error": str(error)}

            print(f"[Tool] {function_name}({function_args})")
            print(f"[Tool result] {result}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(result),
                }
            )

    return "I could not complete the specialist task within the tool limit."


def calculation_specialist(query, context):
    system_prompt = """You are the Calculation Specialist.

Handle math-heavy requests accurately.

You have two tools:
- calculate
- unit_converter

Use the tools for calculations instead of doing arithmetic mentally.

Show important steps when useful.

Return only the final answer to the user, not internal
routing or handoff details."""

    return run_tool_agent(
        query,
        context,
        system_prompt,
        CALCULATION_TOOLS,
    )


def research_specialist(query, context):
    system_prompt = """You are the Research Specialist.

    Handle factual questions using the web_search tool.

    For questions involving current, recent, ongoing, or latest information,
    search using the current year and current information rather than assuming
    an older year.

    Prefer recent and authoritative sources when the question is time-sensitive.

    Use search results as evidence and mention useful source URLs in the answer.

    Do not invent facts or claim to have searched when the tool was not used.

    Return only the final answer to the user, not internal routing or handoff details."""

    return run_tool_agent(
        query,
        context,
        system_prompt,
        RESEARCH_TOOLS,
    )


def handle_query(query):
    intent, reason = classify_intent(query)

    if intent == "general":
        return generalist_answer(query)

    if intent == "math":
        specialist = "Calculation Specialist"
        specialist_function = calculation_specialist
    else:
        specialist = "Research Specialist"
        specialist_function = research_specialist

    context = {
        "original_query": query,
        "classified_intent": intent,
        "reason": reason,
        "handoff_number": 1,
    }

    print(f"[Handoff] Generalist Agent -> {specialist}")
    print(f"[Handoff reason] {reason}")
    print(f"[Handoff context] {json.dumps(context)}")

    return specialist_function(query, context)
