from dotenv import load_dotenv
import os
from google.adk.tools import ToolContext

load_dotenv()


async def set_session_value(tool_context: ToolContext, key: str, value: str):
    """Sets a value in the tool_context's state dictionary."""
    tool_context.state[key] = value
    return {"status": f"stored '{value}' in '{key}'"}
