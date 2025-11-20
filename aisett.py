from  confyg import ai_token
from openai import OpenAI
import logging
import asyncio
import random


async def generate_resp(prompt, maxretries=5):
    """генерация с экспоненциальной задержкой при ошибках"""
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=ai_token,
    )

    for attempt in range(maxretries):
        try:
            completion = client.chat.completions.create(
                model="qwen/qwen3-4b:free",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            if attempt == maxretries - 1:
                logger.error(f'все попытки завершились {e}')
                return "ИЗвините, сервис временно не доступен, попробуйте позже."

            base_del = 2 ** attempt
            jitter = random.uniform(0.1, 0.5)
            delay = base_del + jitter

            logger.warning(f'Попытка {attempt + 1} {e} не удалась. Повтор через {delay:.1f}')

            await asyncio.sleep(delay)
