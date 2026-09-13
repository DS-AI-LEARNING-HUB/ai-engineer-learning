import base64
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import fitz

load_dotenv()

client = OpenAI(
    api_key=os.environ["DATABRICKS_TOKEN"],
    base_url=f"{os.environ['DATABRICKS_HOST']}/serving-endpoints",
)


def caption_image(image_bytes: bytes) -> str:
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:image/png;base64,{image_b64}"
    response = client.chat.completions.create(
        model="databricks-claude-opus-5",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this chart in 2-3 sentences, including the specific data values shown."},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            }
        ],
    )
    return response.choices[0].message.content


def pdf_to_text(pdf_path: Path) -> str:
    """Extract a PDF into ONE unified text string, in original reading order,
    with each embedded image replaced by a captioned description in-place.
    """
    doc = fitz.open(pdf_path)
    pieces: list[str] = []

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        blocks.sort(key=lambda b: b["bbox"][1])

        for block in blocks:
            if block["type"] == 0:
                text = "".join(
                    span["text"] for line in block["lines"] for span in line["spans"]
                ).strip()
                if text:
                    pieces.append(text)

            elif block["type"] == 1:
                caption = caption_image(block["image"])
                pieces.append(f"[Image description: {caption}]")

    doc.close()
    return "\n\n".join(pieces)
