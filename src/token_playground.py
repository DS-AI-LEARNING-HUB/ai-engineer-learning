import truststore
truststore.inject_into_ssl()

import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

texts = [
    "Hello, world!",
    "unbelievable",
    "Databricks Foundation Model APIs are OpenAI-compatible.",
    "I'm learning GenAI while working full-time at NTT.",
]

for text in texts:
    tokens = encoding.encode(text)
    decoded_pieces = [encoding.decode([t]) for t in tokens]
    print(f"\nText: {text!r}")
    print(f"Token count: {len(tokens)}")
    print(f"Pieces: {decoded_pieces}")
