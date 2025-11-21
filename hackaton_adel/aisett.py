from  confyg import ai_token
from openai import OpenAI


async def generate_resp(prompt, maxretries=5):
    """генерация ответа с ии"""
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=ai_token,)

    completion = client.chat.completions.create(
            model="qwen/qwen3-4b:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    completion = completion.choices[0].message.content
    messages = [
        {"role": "user", "content": prompt},
        {
            "role": "assistant",
            "content": completion,
            # "reasoning_details": completion.reasoning_details  # Pass back unmodified
        },
        {"role": "user", "content": prompt}
    ]
    # Second API call - model continues reasoning from where it left off
    response2 = client.chat.completions.create(
        model="x-ai/grok-4.1-fast:free",
        messages=messages,
        extra_body={"reasoning": {"enabled": True}}
    )
    return completion