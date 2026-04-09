import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
from google.adk.agents import Agent
from google.adk.models import Gemini

agent = Agent(name="test", model=Gemini(model=os.getenv("MODEL")), instruction="say hello")

async def test():
    events = agent.async_stream_query(user_id="1", message="hello")
    print(events)
    async for event in events:
        print(type(event))
        if isinstance(event, dict):
            print("is dict. keys:", event.keys())

asyncio.run(test())
