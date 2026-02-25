import os
import aiohttp
import asyncio
from dotenv import load_dotenv
import logging

from app.config.config import PROMT_AI

load_dotenv()
TOKEN = os.getenv("TOKEN_OR_API")

logger = logging.getLogger(__name__)

class AI:
    def __init__(self):
        self.api_key = os.getenv("TOKEN_OR_API")
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "openrouter/free"

    async def send_request(self, message: str, max_token: int = 300, temperature: float = 1.0):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "max_token": max_token,
            "temperature": temperature
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=payload, headers=headers) as resp:
                data = await resp.json()

        if "error" in data:
            error = data["error"]
            raise Exception(f"Open Router error API: {error}")

        if data["choices"][0]["message"]["content"] != "":
            return data["choices"][0]["message"]["content"]
        return data["choices"][0]["message"]["reasoning"]

    async def get_avito_text(self, data):
        promt = PROMT_AI[data["category"]]
        data["equipment"] = ", ".join(data["equipment"])
        promt = promt.format(**data)
        return await self.send_request(promt)

async def main():
    ai = AI()
    data = {
        'category': 'car',
        'equipment': ['climate_control', 'rear_view_camera', 'gps'],
        'car_make': 'toyota',
        'model': 'Prius',
        'year_manufacture': '2022',
        'mileage': '130000',
        'count_owner': '2',
        'count_accidents': '0',
        'body_condition': 'Хорошее',
        'engine_condition': 'Отличное',
        'reason_for_sale': 'Нужны деньги',
        'additional': 'Нет'}
    resp = await ai.get_avito_text(data)
    print(f"Response AI {resp}")

if __name__ == "__main__":
    asyncio.run(main())