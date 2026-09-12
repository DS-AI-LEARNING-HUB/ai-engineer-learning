import os
from dotenv import load_dotenv
from openai import OpenAI

# Reads DATABRICKS_HOST / DATABRICKS_TOKEN from the .env file at project root
# into environment variables, so we never hardcode secrets in this file.
load_dotenv()

# The openai SDK works here because Databricks Foundation Model APIs expose
# an OpenAI-compatible interface — same client, just pointed at Databricks
# instead of OpenAI's servers via base_url.
client = OpenAI(
    api_key=os.environ["DATABRICKS_TOKEN"],
    base_url=f"{os.environ['DATABRICKS_HOST']}/serving-endpoints",
)


def ask(messages: list[dict], label: str) -> None:
    """Send one list of chat messages to the model and print the reply.

    `messages` is the core unit of an LLM API call: an ordered list of
    {"role": ..., "content": ...} dicts. The roles are:
      - "system": sets behavior/persona for the whole conversation
      - "user": what the human is asking
      - "assistant": a prior model reply (used to show few-shot examples,
        or to continue a multi-turn conversation)
    """
    response = client.chat.completions.create(
        model="databricks-claude-opus-5",
        messages=messages,
    )
    print(f"\n--- {label} ---")
    print(response.choices[0].message.content)


# 1. Zero-shot: just ask directly, no examples given.
# Works fine for simple/common tasks, but the model has to guess the exact
# format you want (e.g. will it reply "negative", "Negative", or a full
# sentence? You don't control that here).
ask(
    messages=[{"role": "user", "content": "Classify sentiment: 'The onboarding process was confusing.'"}],
    label="Zero-shot",
)

# 2. Few-shot: we show 2 example Q&A pairs as fake prior turns (user asks,
# assistant answers) before asking the real question. The model picks up
# the pattern — a single lowercase word, no punctuation — and mimics it
# for the real question. This is how you steer output format without
# needing tool/function calling.
ask(
    messages=[
        {"role": "user", "content": "Classify sentiment: 'I love this product!'"},
        {"role": "assistant", "content": "positive"},
        {"role": "user", "content": "Classify sentiment: 'This is the worst experience ever.'"},
        {"role": "assistant", "content": "negative"},
        {"role": "user", "content": "Classify sentiment: 'The onboarding process was confusing.'"},
    ],
    label="Few-shot",
)

# 3. System prompt: sets a persona/constraint that applies to the whole
# exchange, independent of what the user asks. Here it forces a terse,
# 2-sentence-max code-reviewer voice regardless of the question's phrasing.
ask(
    messages=[
        {"role": "system", "content": "You are a terse code reviewer. Answer in at most 2 sentences."},
        {"role": "user", "content": "What's wrong with using a mutable default argument in Python?"},
    ],
    label="System prompt (terse persona)",
)

# 4. Chain-of-thought: explicitly asking the model to "think step by step"
# gives it room to work through intermediate reasoning (as output tokens)
# before committing to a final answer, which improves accuracy on
# arithmetic/logic-style questions.
ask(
    messages=[{"role": "user", "content": "A train travels 60 miles in 45 minutes. What is its speed in mph? Think step by step."}],
    label="Chain-of-thought",
)

# 5. Structured JSON via prompting: asking for "ONLY valid JSON" in plain
# language. This usually works but isn't guaranteed — the model can still
# wrap the JSON in a sentence or markdown code fence. Tool/function calling
# (a later lesson) is the more reliable way to force a schema.
ask(
    messages=[
        {
            "role": "user",
            "content": (
                "Extract the person's name and age from this text, "
                "respond ONLY with valid JSON like {\"name\": ..., \"age\": ...}: "
                "'Rohan is a 29-year-old software engineer.'"
            ),
        }
    ],
    label="Structured JSON",
)
