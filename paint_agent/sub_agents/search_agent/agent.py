import os
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.tools import VertexAiSearchTool, ToolContext
from google.genai import types


load_dotenv()

RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=1, max_delay=3, attempts=30)

SEARCH_ENGINE_PATH = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/global/collections/default_collection/engines/{os.getenv('SEARCH_ENGINE_ID')}"
paint_search_tool = VertexAiSearchTool(search_engine_id=SEARCH_ENGINE_PATH)

search_agent = Agent(
    name="search_agent",
    model=Gemini(model=os.getenv("MODEL"), retry_options=RETRY_OPTIONS),
    instruction="""
    If the user asked for specific paints, look up information on requested paints.
    Otherwise, provide the user information about all Cymbal Shops paints, including price
    and coverage rate.
    """,
    tools=[paint_search_tool],
)
