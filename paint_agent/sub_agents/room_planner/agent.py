import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
from .sub_agents.coverage_calculator.agent import coverage_calculator_agent

load_dotenv()

RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=1, max_delay=3, attempts=30)
# IMG_PATH_1 = f"https://storage.cloud.google.com/{os.getenv("RESOURCES_BUCKET")}/project_paint.png"
IMG_PATH_1 = f"{ASSETS_PATH}/project_paint.png"
IMG_PATH_2 = f"{ASSETS_PATH}/surecoverage.png"
IMG_PATH_3 = f"{ASSETS_PATH}/ecogreens.png"
IMG_PATH_4 = f"{ASSETS_PATH}/forever_paint.png"

room_planner_agent = Agent(
    name="room_planner_agent",
    model=Gemini(model=os.getenv("MODEL"), retry_options=RETRY_OPTIONS),
    description="""
        after paint product is selected, determine how many rooms and
        present color options.""",
    instruction=f"""
    - Find out how many rooms the user would like to paint and what we should call each room.
    - Based on the {{SELECTED_PAINT?}}, show the corresponding images
      in an img tag with a height attribute of 300px:
        - Project Paint: {IMG_PATH_1}
        - SureCoverage: https://storage.cloud.google.com/{os.getenv("RESOURCES_BUCKET")}/surecoverage.png
        - EcoGreen: https://storage.cloud.google.com/{os.getenv("RESOURCES_BUCKET")}/ecogreens.png
        - Forever Paint: https://storage.cloud.google.com/{os.getenv("RESOURCES_BUCKET")}/forever_paint.png
    - Have them pick a color for each room. 
    - To calculate the paint needed for each room, transfer to the 'coverage_calculator_agent'
    """,
    sub_agents=[coverage_calculator_agent],
)
