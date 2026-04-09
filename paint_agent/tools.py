from dotenv import load_dotenv
import os
from google.adk.tools import ToolContext

load_dotenv()


async def set_session_value(tool_context: ToolContext, key: str, value: str):
    """Sets a value in the tool_context's state dictionary."""

    return {"status": "tool not implemented"}
