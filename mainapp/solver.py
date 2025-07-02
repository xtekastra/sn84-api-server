import openai
import traceback
import json
from django.conf import settings
PROMPT = {
    "checkbox": """Extract the selected text from this image. Give me the result only as python list format like this: ["XXX", "XXX"], DO NOT include this kind of string: **```python**.""",
    "encircle": """Extract the text enclosed or circled in this image. Give me the result only as python list format like this: ["XXX", "XXX"], DO NOT include this kind of string: **```python**.""",
    "highlight": """Extract the highlighted text from this image.  Give me the result only as python list format like this: ["XXX", "XXX"], DO NOT include this kind of string: **```python**.""",
    "doc-class": """Identify and classify the type or category of this document. Give me the result only as python list format like this: ["XXX", "XXX"], DO NOT include this kind of string: **```python**.""",
    "doc-parse": """Extract and clearly structure the main content from this document. Give me the result only as python list format like this: ["XXX", "XXX"], DO NOT include this kind of string: **```python**.""",
}

async def solve(image: str, request_id: str, task_type: str):
    try:
        p = """Extract and clearly structure the main content from this document. Give me the result only as python list format like this: ["XXX", "XXX"], DO NOT include this kind of string: **```python**."""
        if task_type in PROMPT:
            p = PROMPT[task_type]
            messages = [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": p},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{image}",
                    },
                ]
            }
        ]

        client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        response = await client.responses.create(
            model=settings.OPENAI_MODEL,
            input=messages,
        )
        
        return str(response.output_text)

    except Exception as e:
        print(f"Error in forward: {e}")
        traceback.print_exc()
        return "[]"
