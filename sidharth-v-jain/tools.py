import ast
import math
from ddgs import DDGS

# ---------- Calculator ----------

ALLOWED_NAMES = {
    "pi": math.pi,
    "e": math.e,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "factorial": math.factorial,
}

ALLOWED_NODES = {
    ast.Expression,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.Mod,
    ast.FloorDiv,
    ast.USub,
    ast.UAdd,
    ast.Name,
    ast.Call,
}


def calculate(expression):
    try:
        tree = ast.parse(expression, mode="eval")

        for node in ast.walk(tree):
            if type(node) not in ALLOWED_NODES:
                raise ValueError("Unsupported expression")

            if isinstance(node, ast.Name) and node.id not in ALLOWED_NAMES:
                raise ValueError(f"Unknown name: {node.id}")

            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name):
                    raise ValueError("Unsupported function")
                if node.func.id not in ALLOWED_NAMES:
                    raise ValueError(f"Unknown function: {node.func.id}")

        value = eval(
            compile(tree, "<calculator>", "eval"),
            {"__builtins__": {}},
            ALLOWED_NAMES,
        )

        return {"result": value}

    except Exception as error:
        return {"error": str(error)}


# ---------- Unit converter ----------

LENGTH_TO_METER = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1,
    "km": 1000,
    "in": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144,
    "mi": 1609.344,
}

MASS_TO_KG = {
    "mg": 0.000001,
    "g": 0.001,
    "kg": 1,
    "lb": 0.45359237,
    "oz": 0.028349523125,
}

TIME_TO_SECOND = {
    "ms": 0.001,
    "s": 1,
    "min": 60,
    "h": 3600,
    "day": 86400,
}


def unit_converter(value, from_unit, to_unit):
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    if from_unit in LENGTH_TO_METER and to_unit in LENGTH_TO_METER:
        base_value = value * LENGTH_TO_METER[from_unit]
        return {"result": base_value / LENGTH_TO_METER[to_unit], "unit": to_unit}

    if from_unit in MASS_TO_KG and to_unit in MASS_TO_KG:
        base_value = value * MASS_TO_KG[from_unit]
        return {"result": base_value / MASS_TO_KG[to_unit], "unit": to_unit}

    if from_unit in TIME_TO_SECOND and to_unit in TIME_TO_SECOND:
        base_value = value * TIME_TO_SECOND[from_unit]
        return {"result": base_value / TIME_TO_SECOND[to_unit], "unit": to_unit}

    if from_unit in {"c", "celsius"} and to_unit in {"f", "fahrenheit"}:
        return {"result": (value * 9 / 5) + 32, "unit": "F"}

    if from_unit in {"f", "fahrenheit"} and to_unit in {"c", "celsius"}:
        return {"result": (value - 32) * 5 / 9, "unit": "C"}

    if from_unit in {"c", "celsius"} and to_unit in {"k", "kelvin"}:
        return {"result": value + 273.15, "unit": "K"}

    if from_unit in {"k", "kelvin"} and to_unit in {"c", "celsius"}:
        return {"result": value - 273.15, "unit": "C"}

    if from_unit in {"f", "fahrenheit"} and to_unit in {"k", "kelvin"}:
        celsius = (value - 32) * 5 / 9
        return {"result": celsius + 273.15, "unit": "K"}

    if from_unit in {"k", "kelvin"} and to_unit in {"f", "fahrenheit"}:
        fahrenheit = (value - 273.15) * 9 / 5 + 32
        return {"result": fahrenheit, "unit": "F"}

    raise ValueError("Unsupported or incompatible units")


# ---------- Web search ----------

def web_search(query, max_results=10):
    try:
        max_results = min(max_results, 10)

        results = DDGS().text(
            query,
            max_results=max_results
        )

        formatted_results = []

        for result in results:
            formatted_results.append(
                {
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", ""),
                }
            )

        return {
            "query": query,
            "results": formatted_results,
        }

    except Exception as error:
        return {
            "query": query,
            "results": [],
            "error": str(error),
        }

# ---------- Groq tool schemas ----------

CALCULATION_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression accurately.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A mathematical expression such as 25 * 4 + 10.",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "unit_converter",
            "description": "Convert a numeric value between compatible units.",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {
                        "type": "number",
                        "description": "The numeric value to convert.",
                    },
                    "from_unit": {
                        "type": "string",
                        "description": "The source unit, such as km, m, kg, lb, C, F.",
                    },
                    "to_unit": {
                        "type": "string",
                        "description": "The target unit, such as m, km, kg, lb, C, F.",
                    },
                },
                "required": ["value", "from_unit", "to_unit"],
            },
        },
    },
]

RESEARCH_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for factual information and recent sources.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The web search query.",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of search results.",
                        "minimum": 1,
                        "maximum": 10,
                    },
                },
                "required": ["query"],
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "calculate": calculate,
    "unit_converter": unit_converter,
    "web_search": web_search,
}
