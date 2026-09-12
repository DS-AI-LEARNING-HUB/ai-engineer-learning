import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ["DATABRICKS_TOKEN"],
    base_url=f"{os.environ['DATABRICKS_HOST']}/serving-endpoints",
)

# This schema describes a fake "tool" called extract_person. We never
# actually implement/run this function — its only purpose is to force the
# model to return arguments matching this exact shape.
tools = [
    {
        "type": "function",
        "function": {
            "name": "extract_person",
            "description": "Extract a person's name and age from text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                },
                "required": ["name", "age"],
            },
        },
    }
]

response = client.chat.completions.create(
    model="databricks-claude-opus-5",
    messages=[
        {
            "role": "user",
            "content": "Rohan is a 29-year-old software engineer. Extract his info.",
        }
    ],
    tools=tools,
    tool_choice="auto",  # let the model decide whether/which tool to call
)

message = response.choices[0].message

if message.tool_calls:
    call = message.tool_calls[0]
    print("Tool called:", call.function.name)
    print("Raw arguments string:", call.function.arguments)

    # arguments come back as a JSON string — parse it into a real dict
    args = json.loads(call.function.arguments)
    print("Parsed arguments:", args)
    print("Name:", args["name"], "| Age:", args["age"])
else:
    print("Model didn't call a tool, replied instead:", message.content)
